from django.contrib import admin
from .models import CustomUser,Task,SmallTask,Motivation

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(SmallTask)
admin.site.register(Motivation)
