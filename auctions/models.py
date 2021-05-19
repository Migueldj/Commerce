from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import tree


class User(AbstractUser):
    pass

class Category(models.Model):
    options = models.CharField(max_length=64)

    def __str__(self):
        return self.options 

class Commentary(models.Model):
    comment = models.CharField(max_length = 100)

class Listing(models.Model):
    title = models.CharField(max_length=64, null = True)
    description = models.TextField()
    category = models.ForeignKey(Category, blank = True,  on_delete=models.PROTECT, related_name="Filter")
    imageURL = models.URLField()
    bid = models.IntegerField()
    user = models.ForeignKey(User, null = True, on_delete=CASCADE, related_name= "UserListings")
    comments = models.ManyToManyField(Commentary, null = True, blank = True, related_name = "ListingComments")
    active = models.BooleanField(default = True)

    def __str__(self):
        return self.title


