from django.contrib import admin

from .models import Workday
from .models import Task

admin.site.register(Workday)
admin.site.register(Task)
