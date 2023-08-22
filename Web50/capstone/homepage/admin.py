from django.contrib import admin
from django.contrib.admin import actions
from .models import Subscriber, BlogPost


class SelectAllAdmin(admin.ModelAdmin):
    actions = [actions.delete_selected]


class SubscriberAdmin(SelectAllAdmin):
    list_display = ("name", "email", "message")
    list_editable = ("email", "message")
    list_per_page = 20


admin.site.register(BlogPost)

admin.site.register(Subscriber, SubscriberAdmin)
