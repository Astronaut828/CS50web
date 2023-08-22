from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f"{self.username} ({self.email})"


User = get_user_model()

class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    listing_title = models.CharField(max_length=255, default='')
    listing_description = models.TextField(default='')
    listing_pic = models.URLField(default='')
    category = models.CharField(max_length=255, default='Uncategorized')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='listings')
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listings')

    def __str__(self):
        return self.listing_title


class ItemComment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.listing_title}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_watchlist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Watchlist Item: {self.listing.listing_title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid {self.bid} on {self.listing.listing_title} by {self.bidder.username}"