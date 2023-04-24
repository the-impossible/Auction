from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Auction_auth.models import *

# Register your models here.


class UserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'name', 'picture', 'address', 'date_joined',
                    'last_login', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'phone', 'address')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAdmin)
