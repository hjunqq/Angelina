from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.empty_value_display = '(None)'

class UserLogInfoList(admin.ModelAdmin):
    list_display = ('pk','user','logInIP','logInTime','logOutTime','UserAgent')

class DayMoodList(admin.ModelAdmin):
    list_display = ('pk','time','author','score')


admin.site.register(DayMood,DayMoodList)
admin.site.register(DayScore)
admin.site.register(MonthScore)
admin.site.register(YearScore)
admin.site.register(KeyWord)
admin.site.register(UserLogInfo,UserLogInfoList)

