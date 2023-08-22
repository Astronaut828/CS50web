from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)


class Following(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.user} follows {self.following_user}"


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body_text = models.TextField()
    timestamp = models.DateTimeField()
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.body_text


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']

class FollowingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'following_user']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'body_text', 'timestamp', 'likes']
    list_editable = ['body_text', 'timestamp', 'likes']

admin.site.register(User, UserAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(Post, PostAdmin)
