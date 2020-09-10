from django.contrib import admin

# Register your models here.

from .models import Profile, LeaveApplication

admin.site.register(Profile)
admin.site.register(LeaveApplication)