from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('item/<int:listing_id>/', views.item, name='item'),
    path("login", views.login_view, name="login"),
    path("categories", views.categories, name="categories"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bought", views.bought, name="bought"),
    path("create", views.create, name="create"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit_comment/<int:listing_id>", views.submit_comment, name="submit_comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.add_to_watchlist, name="remove_from_watchlist"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
]
