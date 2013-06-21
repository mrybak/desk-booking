# coding=utf-8
from django.test import TestCase
from booking.models import *


class BookingTest(TestCase):
    def test_example(self):
        u = User()
        u.save()
        # mamy jeden pokój w którym są trzy biurka
        r = Room()
        r.save()
        d = []
        for desk in [1, 2, 3]:
            temp_d = Desk()
            temp_d.room = r
            temp_d.save()
            d.append(temp_d)
        # z ceną bazową 100zł w kwietniu
        bp = BasePrice()
        bp.price = 100
        bp.save()
        apr = BasePricePeriod()
        apr.base_price = bp
        apr.from_date = datetime.datetime(2013, 4, 01)
        apr.to_date = datetime.datetime(2013, 4, 30)
        apr.save()
        # Mamy zniżkę 50% za wynajęcie biurek na co najmniej 2 osobogodziny...
        phd = PersonHourDiscount()
        phd.discount_percents = 50
        phd.min_hours = 2
        phd.save()
        # ...w godzinach 10-12 w kwietniu.
        phdp = PersonHourDiscountPeriod()
        phdp.person_hour_discount = phd
        phdp.from_hour = 10
        phdp.to_hour = 12  # exclusive!
        phdp.from_date = datetime.datetime(2013, 4, 01)
        phdp.to_date = datetime.datetime(2013, 4, 30)
        phdp.save()

        # Mamy zniżkę 50% za wynajęcie całego pokoju.
        wrd = WholeRoomDiscount()
        wrd.discount_percents = 50
        wrd.save()

        wrdp = WholeRoomDiscountPeriod()
        wrdp.whole_room_discount = wrd
        wrdp.from_date = datetime.datetime(2013, 4, 01)
        wrdp.to_date = datetime.datetime(2013, 4, 30)
        wrdp.save()

        # Zarezerwować pokój w godzinach 10-16 1 kwietnia dla dwóch osób
        rp1 = ReservationPeriod()
        rp1.from_hour = 10
        rp1.to_hour = 16  # exclusive!
        rp1.from_date = datetime.datetime(2013, 4, 01)
        rp1.to_date = datetime.datetime(2013, 4, 01)
        rp1.user = u
        rp1.final_price = -1
        rp1.save()

        r1 = Reservation()
        r1.desk = d[0]
        r1.period = rp1
        r1.user = u
        r1.save()
        r2 = Reservation()
        r2.desk = d[1]
        r2.period = rp1
        r2.user = u
        r2.save()

        # Zarezerwować pokój w godzinach 10-12 2 kwietnia dla trzech osób
        rp2 = ReservationPeriod()
        rp2.from_hour = 10
        rp2.to_hour = 12  # exclusive!
        rp2.from_date = datetime.datetime(2013, 4, 02)
        rp2.to_date = datetime.datetime(2013, 4, 02)
        rp2.user = u
        rp2.final_price = -1
        rp2.save()


        r3 = Reservation()
        r3.desk = d[0]
        r3.period = rp2
        r3.user = u
        r3.save()

        r4 = Reservation()
        r4.desk = d[1]
        r4.period = rp2
        r4.user = u
        r4.save()

        r5 = Reservation()
        r5.desk = d[2]
        r5.period = rp2
        r5.user = u
        r5.save()

        # po znizce 50% za osobogodziny w godzinach 10-12; 12-16 brak znizek
        self.assertEquals(rp1.get_final_price(), 500)
        # jw. + znizka 50% za wynajecie pokoju; razem znizka 75%
        self.assertEquals(rp2.get_final_price(), 50)

