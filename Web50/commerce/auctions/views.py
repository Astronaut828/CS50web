from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal

from .models import User, Listing, ItemComment, Watchlist, Bid


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):

    # create new listing
    if request.method == "POST":
        listing_title = request.POST["listing_title"]
        listing_description = request.POST["listing_description"]
        listing_pic = request.POST["listing_pic_url"]
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]
        user = request.user
        is_active = True
        created_time = timezone.now()

        # save new listing information
        new_listing = Listing(
            listing_title=listing_title,
            listing_description=listing_description,
            listing_pic=listing_pic,
            category=category,
            starting_bid=starting_bid,
            user=user,
            is_active=is_active,
            created_time=created_time
        )
        new_listing.save()

        return redirect(reverse("index"))

    else:
        return render(request, "auctions/create.html")


def item(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    on_watchlist = False
    auction_winner = None

    if request.user.is_authenticated:
        # Check if the listing is on the user's watchlist
        on_watchlist = Watchlist.objects.filter(listing=listing, user=request.user, on_watchlist=True).exists()

        # Check if the auction is closed and the user is the winner
        if listing.is_closed and listing.highest_bidder == request.user:
            auction_winner = request.user

    return render(request, "auctions/item.html", {
        "listing": listing,
        "on_watchlist": on_watchlist,
        "auction_winner": auction_winner
    })


@login_required
def submit_comment(request, listing_id):
    if request.method == "POST":
        comment_text = request.POST["add_comment"]
        listing = get_object_or_404(Listing, id=listing_id)

        # Create and save the comment
        comment = ItemComment(listing=listing, author=request.user, comment=comment_text)
        comment.save()

    return redirect(reverse("item", args=[listing_id]))

# Returns category page and lets user pic
@login_required
def categories(request):
    return render(request, "auctions/categories.html")

# Shows all listings in a specific category
@login_required
def category(request):
    category_name = request.GET.get('category')
    listings = Listing.objects.filter(category=category_name, is_active=True)
    return render(request, "auctions/category.html", {
        "category_name": category_name,
        "listings": listings
    })

# Lists all items a user bought
@login_required
def bought(request):
    user = request.user
    bought_items = Listing.objects.filter(highest_bidder=user, is_closed=True)

    return render(request, "auctions/bought.html", {
        "bought_items": bought_items,
    })

# Displays all items a user has in his watchlist
@login_required
def watchlist(request):
    user = request.user
    watchlist_items = Watchlist.objects.filter(user=user, on_watchlist=True)
    user_watchlist_items = [watchlist.listing for watchlist in watchlist_items]

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": user_watchlist_items,
    })

# Function for watchlist button (add / remove)
@login_required
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, id=listing_id)
        watchlist_item, created = Watchlist.objects.get_or_create(listing=listing, user=request.user)
        if created:
            watchlist_item.on_watchlist = True
        else:
            watchlist_item.on_watchlist = not watchlist_item.on_watchlist
        watchlist_item.save()

    return redirect(reverse("item", args=[listing_id]))


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        bid_amount = Decimal(request.POST["place_bid"])
        listing = get_object_or_404(Listing, id=listing_id)
        #checking if bid amount is larger then current listing price
        if bid_amount <= listing.current_price or bid_amount < listing.starting_bid:
            bid_error = "Bid amount must be greater than the current price."
            return render(request, "auctions/item.html", {
                "listing": listing,
                "bid_error": bid_error
            })

        bidder = request.user
        # saving the valid bid made by the user
        bid = Bid(
            listing=listing,
            bidder=bidder,
            bid=bid_amount,
            created_time=timezone.now()
        )
        bid.save()

        listing.current_price = bid_amount
        listing.save()

        messages.success(request, "Bid placed successfully.")
        return redirect(reverse("item", args=[listing_id]))

    return redirect(reverse("item", args=[listing_id]))

# Function to close a listing and set it to inactive
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    #check if viewing user is the creator of the item
    if request.user == listing.user and not listing.is_closed:
        if listing.current_price > listing.starting_bid:
            listing.highest_bidder = listing.bids.order_by('-bid').first().bidder
        else:
            listing.highest_bidder = None
        listing.is_closed = True
        listing.is_active = False  # Set is_active to False
        listing.save()
        messages.success(request, "Auction closed successfully.") #success message
    else:
        messages.error(request, "You are not authorized to close this auction.")
    return redirect(reverse("item", args=[listing_id]))
