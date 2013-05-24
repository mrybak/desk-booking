# coding=utf-8
import datetime
import logging
import time
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

log = logging.getLogger('myapp.logger')

class Room(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    def count_all_desks(self):
        return Desk.objects.filter(room__id=self.id).count()

    def count_free_desks(self, free_desks_ids):
        return Desk.objects.filter(id__in=free_desks_ids, room__id=self.id).count()

    def is_free(self, free_desks_ids):
        return self.count_all_desks() == self.count_free_desks(free_desks_ids)

    def __unicode__(self):
        return self.street + " , " + self.city


class Desk(models.Model):
    room = models.ForeignKey(Room)
    description = models.TextField()
    def __unicode__(self):
        return str(self.room)

class BasePrice(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    def __unicode__(self):
        return self.name

class WholeRoomDiscount(models.Model):
    name = models.CharField(max_length=200)
    discount_percents = models.IntegerField()
    def __unicode__(self):
        return self.name

class PersonHourDiscount(models.Model):
    name = models.CharField(max_length=200)
    min_hours = models.IntegerField()
    discount_percents = models.IntegerField()
    def __unicode__(self):
        return self.name

class Period(models.Model):
    # inclusive
    from_date = models.DateField()
    # inclusive
    to_date = models.DateField()
    # inclusive
    from_hour = models.IntegerField(blank=True, null=True)
    # exclusive
    to_hour = models.IntegerField(blank=True, null=True)
    # days of week
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)

    # list of weekday codes
    def getDayset(self):
        dayset = []
        if self.monday:
            dayset.append(0)
        if self.tuesday:
            dayset.append(1)
        if self.wednesday:
            dayset.append(2)
        if self.thursday:
            dayset.append(3)
        if self.friday:
            dayset.append(4)
        if self.saturday:
            dayset.append(5)
        if self.sunday:
            dayset.append(6)
        return dayset

    # list of timestamps for all hours in this period
    def getHourset(self):
        start = time.time()
        hourset = []
        one_day = datetime.timedelta(days=1)
        dayset = self.getDayset()
        start_hour = self.from_hour if self.from_hour != None else 0
        end_hour = self.to_hour if self.to_hour != None else 24
        # iterate through all days of a period
        cur_day = self.from_date
        while cur_day <= self.to_date:
            # if current day is within chosen days of week
            if dayset.count(cur_day.weekday()):
                for cur_hour in range(start_hour, end_hour):
                    cur_datetime = datetime.datetime(cur_day.year, cur_day.month, cur_day.day, cur_hour)
                    # DEBUG: hourset.append(cur_datetime)
                    timestamp = time.mktime(cur_datetime.timetuple())
                    hourset.append(timestamp)
            cur_day += one_day
        #log.debug("getHourset lasted: ")
        #log.debug(time.time() - start)

        return hourset

    # does this period have a non-void intersection with given period?
    def intersects_with(self, other_period):
        # log.debug("intersects_with start")
        # start = time.time()
        result = False
        self_hs = self.getHourset()
        for hour in other_period.getHourset():
            if self_hs.count(hour):
                result = True

        # log.debug("intersects_with end, it lasted:")
        # log.debug(time.time() - start)
        return result

    # does every hour of this period have some BasePrice set?
    def get_price(self):
        log.debug("has_baseprice start")
        start = time.time()
        all_base_hours = []
        all_base_prices = []
        for bpp in BasePricePeriod.objects.all():
            hs = bpp.getHourset()
            all_base_hours.extend(hs)
            for _ in hs:
                all_base_prices.append(bpp.base_price.price)

        result = True

        for hour in self.getHourset():
            found = False
            if not all_base_hours.count(hour):
                result = False
        # if BasePrice is defined, count price for this period
        if result:
            hour_prices = dict(zip(all_base_hours, all_base_prices))
            price = 0
            for hour in self.getHourset():
                price += hour_prices.get(hour)
        else:
            price = -1

        log.debug("has_baseprice end, it lasted:")
        log.debug(time.time() - start)
        log.debug("price: " + str(price))

        return price

    def find_free_desks_ids(self,city=""):
        free_desks_ids = []
        for desk in Desk.objects.filter(room__city__contains=city):
            free_desks_ids.append(desk.id)
        for resv in Reservation.objects.all():
            if resv.period.intersects_with(self):
                if free_desks_ids.count(resv.desk_id):
                    free_desks_ids.remove(resv.desk_id)
        return free_desks_ids

    def find_free_desks(self, city=""):
        return Desk.objects.filter(id__in=self.find_free_desks_ids(city))

    def __unicode__(self):
        result = "od " + str(self.from_date) + " do " + str(self.to_date) + " w: "
        if self.monday:
            result += "pn "
        if self.tuesday:
            result += "wt "
        if self.wednesday:
            result += "sr "
        if self.thursday:
            result += "czw "
        if self.friday:
            result += "pt "
        if self.saturday:
            result += "sob "
        if self.sunday:
            result += "nd "
        if self.from_hour is None and self.to_hour is None:
            result += " przez caly dzien"
        elif self.from_hour is None:
            result += " do godziny " + str(self.to_hour)
        elif self.to_hour is None:
            result += " od godziny " + str(self.from_hour)
        else:
            result += " w godzinach " + str(self.from_hour) + "-" + str(self.to_hour)
        return result
    
    class Meta:
        abstract = True



class BasePricePeriod(Period):
    base_price = models.ForeignKey(BasePrice)

    def clean(self):
        from django.core.exceptions import ValidationError
        overlapped = False
        for old_bpp in BasePricePeriod.objects.all():
            if old_bpp.intersects_with(self):
                overlapped = True

        # Raise error if given BasePrice overlaps any other in this database
        if overlapped:
            raise ValidationError('Okresy obowiązywania cen bazowych nie mogą na siebie nachodzić.')



class WholeRoomDiscountPeriod(Period):
    whole_room_discount = models.ForeignKey(WholeRoomDiscount)

class PersonHourDiscountPeriod(Period):
    person_hour_discount = models.ForeignKey(PersonHourDiscount)

class ReservationPeriod(Period):
    user = models.ForeignKey(User)

class PeriodForm(ModelForm):
    class Meta:
        model = Period

class Reservation(models.Model):
    user = models.ForeignKey(User)
    desk = models.ForeignKey(Desk)
    period = models.ForeignKey(ReservationPeriod)
    def __unicode__(self):
        return "user: " + str(self.user) + ", desk " + str(self.desk) + ", period: " + str(self.period)