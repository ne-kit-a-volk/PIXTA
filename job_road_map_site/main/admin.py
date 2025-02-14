from django.contrib import admin

# Register your models here.
from .models import UserManager, main_user

admin.site.register(main_user)
