from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Auction_auth.models import *

# Register your models here.


class UsersAdmin(UserAdmin):
    list_display = ('email', 'phone', 'name', 'picture', 'address', 'date_joined',
                    'last_login', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone', 'address')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class FurnitureAdmin(UserAdmin):
    list_display = ('furniture_name', 'start_price', 'start_date_and_time', 'end_date_and_time', 'image',
                    'furniture_desc')
    search_fields = ('furniture_name', 'start_price',
                     'furniture_desc', 'start_date_and_time', 'end_date_and_time')
    ordering = ('furniture_name',)
    readonly_fields = ('start_date_and_time', 'end_date_and_time', 'created')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# admin.site.register(User, UsersAdmin)
# admin.site.register(Furniture, FurnitureAdmin)
admin.site.register(Furniture)
admin.site.register(User)
