from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name='search'),
    path("<str:entry>", views.entry, name="entry"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit_entry/", views.edit_entry, name="edit_entry"),
    path("random/", views.random, name="random"),
]
