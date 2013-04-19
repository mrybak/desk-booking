from django.contrib import admin
from booking.models import *

class BasePricePeriodInline(admin.StackedInline):
    model = BasePricePeriod
    extra = 1

class WholeRoomDiscountPeriodInline(admin.StackedInline):
    model = WholeRoomDiscountPeriod
    extra = 1

class PersonHourDiscountPeriodInline(admin.StackedInline):
    model = PersonHourDiscountPeriod
    extra = 1

class BasePriceAdmin(admin.ModelAdmin):
    inlines = [BasePricePeriodInline]

class WholeRoomDiscountAdmin(admin.ModelAdmin):
    inlines = [WholeRoomDiscountPeriodInline]

class PersonHourDiscountAdmin(admin.ModelAdmin):
    inlines = [PersonHourDiscountPeriodInline]

admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(BasePrice, BasePriceAdmin)
admin.site.register(WholeRoomDiscount, WholeRoomDiscountAdmin)
admin.site.register(PersonHourDiscount, PersonHourDiscountAdmin)


