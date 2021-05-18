from django.contrib import admin
from .models import Category, Listing, User
# Register your models here.

admin.site.register(User) # lo agregué para poder modificar usuarios desde admin
admin.site.register(Listing)
admin.site.register(Category)
