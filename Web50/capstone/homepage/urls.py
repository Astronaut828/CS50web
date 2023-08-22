from django.urls import path
from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.index, name="index"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("spotlight", views.spotlight, name="spotlight"),
    path("about", views.about, name="about"),
]