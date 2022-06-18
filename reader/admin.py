from django.contrib import admin
from django.contrib.auth.models import Permission

from reader.models import Reader
from book.models import *
admin.site.register(Reader)
admin.site.register(Permission)
# Register your models here.
