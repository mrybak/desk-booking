# coding=utf-8
from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    def __unicode__(self):
        return self.street + " street, " + self.city


class Desk(models.Model):
    room = models.ForeignKey(Room)
    description = models.TextField()
    def __unicode__(self):
        return "in: " + str(self.room)

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
    def __unicode__(self):
        result = "Od " + str(self.from_date) + " do " + str(self.to_date) + " w: "
        if self.monday:
            result += "poniedziałek, "
        if self.tuesday:
            result += "wtorek, "
        if self.wednesday:
            result += "środę, "
        if self.thursday:
            result += "czwartek, "
        if self.friday:
            result += "piątek, "
        if self.saturday:
            result += "sobotę, "
        if self.sunday:
            result += "niedzielę, "
        if self.from_hour is None and self.to_hour is None:
            result += " przez cały dzień"
        elif self.from_hour is None:
            result += " do godziny " + str(self.to_hour)
        elif self.to_hour is None:
            result += " od godziny " + str(self.from_hour)
        else:
            result += " w godzinach " + str(self.from_hour) + "-" + str(self.from_hour)
        return result
    
    class Meta:
        abstract = True

class BasePricePeriod(Period):
    base_price = models.ForeignKey(BasePrice)
    """
    def clean(self):
        from django.core.exceptions import ValidationError
        # Raise error if given BasePrice overlaps any other in this database
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError('Draft entries may not have a publication date.')
            # Set the pub_date for published items if it hasn't been set already.
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()
    """

class WholeRoomDiscountPeriod(Period):
    whole_room_discount = models.ForeignKey(WholeRoomDiscount)

class PersonHourDiscountPeriod(Period):
    person_hour_discount = models.ForeignKey(PersonHourDiscount)

class ReservationPeriod(Period):
    user = models.ForeignKey(User)

class Reservation(models.Model):
    user = models.ForeignKey(User)
    desk = models.ForeignKey(Desk)
    period = models.ForeignKey(ReservationPeriod)
    def __unicode__(self):
        return "user: " + str(self.user) + ", desk " + str(self.desk) + ", period: " + str(self.period)