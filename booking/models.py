# coding=utf-8
import datetime
import logging
import time
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from numpy.core import multiarray

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
        return self.street + ", " + self.city


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
    # returns number of hours of such an intersection
    def intersects_with(self, other_period):
        # log.debug("intersects_with start")
        # start = time.time()
        result = 0
        self_hs = self.getHourset()
        for hour in other_period.getHourset():
            if self_hs.count(hour):
                result += 1

        # log.debug("intersects_with end, it lasted:")
        # log.debug("intersect by " + str(result))
        return result

    # get price for every hours in this period
    def get_prices(self):
        # log.debug("get_price start")
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
        prices = []
        if result:
            hour_prices = dict(zip(all_base_hours, all_base_prices))
            for hour in self.getHourset():
                prices.append(hour_prices.get(hour))

        # log.debug("get_price end, it lasted:")
        # log.debug(time.time() - start)
        # log.debug("prices: " + str(prices))

        return prices

    def get_price(self):
        price = sum(self.get_prices())
        if price > 0:
            return price
        else:
            return -1 # this sucks

    def find_free_desks_ids(self,city=""):
        free_desks_ids = []
        for desk in Desk.objects.filter(room__city__contains=city):
            free_desks_ids.append(desk.id)
        for resv in Reservation.objects.all():
            if resv.period.intersects_with(self):
                if free_desks_ids.count(resv.desk_id):
                    free_desks_ids.remove(resv.desk_id)
        # log.debug("free_desks_ids:")
        # log.debug(free_desks_ids)
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
    final_price = models.IntegerField(default=-1)

    def apply_personhoursdiscount(self):
        hs = self.getHourset()
        multipliers = []

        applicable_discounts = []
        for phd in PersonHourDiscountPeriod.objects.all():
            # could also iterate over all user's reservations...
            if phd.intersects_with(self) >= phd.person_hour_discount.min_hours:
                applicable_discounts.append(phd)
        log.debug("applicable_discounts")
        log.debug(applicable_discounts)

        for hour in hs:
            # start with multiplier 1
            multiplier = 1
            for phd in applicable_discounts:
                if phd.getHourset().count(hour):
                    multiplier = multiplier * (1 - float(phd.person_hour_discount.discount_percents) / 100)
            multipliers.append(multiplier)

        return multipliers

    def apply_wholeroomdiscount(self):
        hs = self.getHourset()
        multipliers = []

        applicable_discounts = []

        for resv in Reservation.objects.filter(user=self.user, period=self):
            log.debug("matching reservation: ")
            log.debug(resv)
            log.debug(Reservation.objects.filter(user=self.user, desk__room=resv.desk.room, period=self).count())
            log.debug(resv.desk.room.count_all_desks())
            if Reservation.objects.filter(user=self.user, desk__room=resv.desk.room, period=self).count() == resv.desk.room.count_all_desks():
                for wrd in WholeRoomDiscountPeriod.objects.all():
                    if wrd.intersects_with(self) and not applicable_discounts.count(wrd):
                        applicable_discounts.append(wrd)


        log.debug("applicable_discounts")
        log.debug(applicable_discounts)

        for hour in hs:
            multiplier = 1
            for wrd in applicable_discounts:
                if wrd.getHourset().count(hour):
                    multiplier = multiplier * (1 - float(wrd.whole_room_discount.discount_percents) / 100)
            multipliers.append(multiplier)

        return multipliers


    def get_final_price(self):
        log.debug("self.final price is: ")
        log.debug(self.final_price)
        if self.final_price == -1:
            log.debug("get_final_price start")
            start = time.time()
            phd_mult = self.apply_personhoursdiscount()
            # start = time.time()
            wrd_mult = self.apply_wholeroomdiscount()

            log.debug("phd_mult")
            log.debug(phd_mult)
            log.debug("wrd_mult")
            log.debug(wrd_mult)

            # final discount multipliers for every hour in self.getHourset
            td_mult = [round(phd_mult[i] * wrd_mult[i],2) for i in range(len(phd_mult))]


            log.debug("tcx_mult")
            log.debug(td_mult)

            # price for every hour in self.getHourset
            prices = self.get_prices()
            log.debug("prices")
            log.debug(prices)

            # price * discount...
            prices_with_discount = [round(td_mult[i] * prices[i],2) for i in range(len(td_mult))]
            log.debug("prices with discount")
            log.debug(prices_with_discount)


            log.debug("get_final_price end, it lasted:")
            log.debug(time.time() - start)
            log.debug("====================================================================")

            # cache result
            self.final_price = int(sum(prices_with_discount))
            self.save()

            log.debug("cached self.final price is: ")
            log.debug(self.final_price)

            return int(sum(prices_with_discount))
        else:
            log.debug("get_final_price from cache")
            log.debug("====================================================================")

            return self.final_price

class PeriodForm(ModelForm):
    class Meta:
        model = Period

class Reservation(models.Model):
    user = models.ForeignKey(User)
    desk = models.ForeignKey(Desk)
    period = models.ForeignKey(ReservationPeriod)
    def __unicode__(self):
        return "user: " + str(self.user) + ", desk " + str(self.desk) + ", period: " + str(self.period)