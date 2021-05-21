from django.db.models.fields import related
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
from django.db.models.query_utils import RegisterLookupMixin
from django.utils import tree


class User(AbstractUser):
    userWatchlist = models.ManyToManyField("Listing", null=True, blank=True, related_name="UserWatchlist")

class Category(models.Model):
    options = models.CharField(max_length=64)

    def __str__(self):
        return self.options 

class Commentary(models.Model):
    comment = models.CharField(max_length = 100)
    user = models.ForeignKey(User, null = True, blank = True, on_delete=CASCADE)
    date = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey("Listing", null=True, on_delete=CASCADE, related_name="Comments")

    def __str__(self):
        return f"User: {self.user} Date: {self.date} Listing: {self.listing} Comment: {self.comment}"

class Listing(models.Model):
    title = models.CharField(max_length=64, null = True)
    description = models.TextField()
    category = models.ForeignKey(Category, blank = True,  on_delete=models.PROTECT, related_name="Filter")
    imageURL = models.URLField()
    bid = models.IntegerField()
    user = models.ForeignKey(User, null = True, on_delete=CASCADE, related_name= "UserListings")
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.title


