from django.db import models

# Create your models here.
class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(default='Default message')

    objects = models.Manager()

    def __str__(self):
        return f"{self.name} ({self.email})"


class BlogPost(models.Model):
    thumbnail = models.URLField()
    featured_link = models.URLField()
    title_link = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()
    website = models.URLField()
    twitter = models.URLField()

    def __str__(self):
        return self.title