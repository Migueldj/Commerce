from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass  

class Category(models.Model):
    options = models.CharField(max_length=64)

    def __str__(self):
        return self.options 

class Listing(models.Model):
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, blank = True,  on_delete=models.PROTECT, related_name="Filter")
    imageURL = models.CharField(max_length=200)
    bid = models.IntegerField()
    
