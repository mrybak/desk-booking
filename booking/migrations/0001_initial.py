# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'booking_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'booking', ['Room'])

        # Adding model 'Desk'
        db.create_table(u'booking_desk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.Room'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'booking', ['Desk'])

        # Adding model 'BasePrice'
        db.create_table(u'booking_baseprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'booking', ['BasePrice'])

        # Adding model 'WholeRoomDiscount'
        db.create_table(u'booking_wholeroomdiscount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discount_percents', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'booking', ['WholeRoomDiscount'])

        # Adding model 'PersonHourDiscount'
        db.create_table(u'booking_personhourdiscount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('min_hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'booking', ['PersonHourDiscount'])

        # Adding model 'BasePricePeriod'
        db.create_table(u'booking_basepriceperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
            ('from_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('to_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('base_price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.BasePrice'])),
        ))
        db.send_create_signal(u'booking', ['BasePricePeriod'])

        # Adding model 'WholeRoomDiscountPeriod'
        db.create_table(u'booking_wholeroomdiscountperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
            ('from_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('to_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('whole_room_discount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.WholeRoomDiscount'])),
        ))
        db.send_create_signal(u'booking', ['WholeRoomDiscountPeriod'])

        # Adding model 'PersonHourDiscountPeriod'
        db.create_table(u'booking_personhourdiscountperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
            ('from_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('to_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('person_hour_discount', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.PersonHourDiscount'])),
        ))
        db.send_create_signal(u'booking', ['PersonHourDiscountPeriod'])

        # Adding model 'ReservationPeriod'
        db.create_table(u'booking_reservationperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_date', self.gf('django.db.models.fields.DateField')()),
            ('to_date', self.gf('django.db.models.fields.DateField')()),
            ('from_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('to_hour', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'booking', ['ReservationPeriod'])

        # Adding model 'Reservation'
        db.create_table(u'booking_reservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('desk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.Desk'])),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['booking.ReservationPeriod'])),
        ))
        db.send_create_signal(u'booking', ['Reservation'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'booking_room')

        # Deleting model 'Desk'
        db.delete_table(u'booking_desk')

        # Deleting model 'BasePrice'
        db.delete_table(u'booking_baseprice')

        # Deleting model 'WholeRoomDiscount'
        db.delete_table(u'booking_wholeroomdiscount')

        # Deleting model 'PersonHourDiscount'
        db.delete_table(u'booking_personhourdiscount')

        # Deleting model 'BasePricePeriod'
        db.delete_table(u'booking_basepriceperiod')

        # Deleting model 'WholeRoomDiscountPeriod'
        db.delete_table(u'booking_wholeroomdiscountperiod')

        # Deleting model 'PersonHourDiscountPeriod'
        db.delete_table(u'booking_personhourdiscountperiod')

        # Deleting model 'ReservationPeriod'
        db.delete_table(u'booking_reservationperiod')

        # Deleting model 'Reservation'
        db.delete_table(u'booking_reservation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'booking.baseprice': {
            'Meta': {'object_name': 'BasePrice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
        },
        u'booking.basepriceperiod': {
            'Meta': {'object_name': 'BasePricePeriod'},
            'base_price': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.BasePrice']"}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'booking.desk': {
            'Meta': {'object_name': 'Desk'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.Room']"})
        },
        u'booking.personhourdiscount': {
            'Meta': {'object_name': 'PersonHourDiscount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_hours': ('django.db.models.fields.IntegerField', [], {})
        },
        u'booking.personhourdiscountperiod': {
            'Meta': {'object_name': 'PersonHourDiscountPeriod'},
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'person_hour_discount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.PersonHourDiscount']"}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'booking.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'desk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.Desk']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.ReservationPeriod']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'booking.reservationperiod': {
            'Meta': {'object_name': 'ReservationPeriod'},
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'booking.room': {
            'Meta': {'object_name': 'Room'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'booking.wholeroomdiscount': {
            'Meta': {'object_name': 'WholeRoomDiscount'},
            'discount_percents': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'booking.wholeroomdiscountperiod': {
            'Meta': {'object_name': 'WholeRoomDiscountPeriod'},
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            'from_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
            'to_hour': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'whole_room_discount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['booking.WholeRoomDiscount']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['booking']