from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from .models import Account

admin.site.register(Account)
admin.site.register(Permission)
# Register your models here.
