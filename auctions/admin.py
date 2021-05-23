from django.contrib import admin
from .models import Bid, Category, Commentary, Listing, User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("userWatchlist",)

admin.site.register(User,UserAdmin) # lo agregué para poder modificar usuarios desde admin
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Commentary)
admin.site.register(Bid)
