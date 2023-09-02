from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    nameofcategory=models.CharField(max_length=64)
    def __str__(self):
        return self.nameofcategory
    

class Bids(models.Model):
    thebid = models.IntegerField(default=0)
    userbid = models.ForeignKey(User, on_delete=models.CASCADE,related_name="userbid", blank=True, null=True)
    def __str__(self):
        return f"{self.thebid}"


class AuctionListings(models.Model):
    name=models.CharField(max_length=64)
    description=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    price=models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="bid")
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner", blank=True, null=True)
    active=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", blank=True, null=True)
    watchlist=models.ManyToManyField(User, blank=True, related_name="watchlist", null=True)
    
    def __str__(self):
        return self.name
    


class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE,related_name="commenter", blank=True, null=True)
    thelist = models.ForeignKey(AuctionListings, on_delete=models.CASCADE,related_name="thelist", blank=True, null=True)
    comments = models.CharField(max_length=200, default="COMMENT")
    
    def __str__(self):
        return self.commenter