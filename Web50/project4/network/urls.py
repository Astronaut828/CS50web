
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user", views.user, name="user"),
    path('user/<int:user_id>/', views.user_page, name='user_page'),
    path('follow-toggle/', views.follow_toggle_view, name='follow-toggle'),
    path('like-toggle/<int:post_id>/', views.like_toggle_view, name='like_toggle'),
    path("following", views.following, name="following"),
    path('update_post/<int:post_id>/', views.UpdatePostView.as_view(), name='update_post'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post/", views.create_post, name="create_post"),
]
