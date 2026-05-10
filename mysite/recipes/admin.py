from django.contrib import admin

from django.contrib import admin
from .models import Recipe

admin.site.register(Recipe) # Без этой строки админка может работать неправильно


# Register your models here.
