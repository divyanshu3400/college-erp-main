from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import CustomUser


class UserModel(UserAdmin):
    pass

# admin.site.register(CustomUser,UserModel)

from django.apps import apps

app_models = apps.get_app_config('student_management_app').get_models()

for model in app_models:
    admin.site.register(model)