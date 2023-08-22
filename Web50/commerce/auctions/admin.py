from django.contrib import admin

from .models import User, Listing, ItemComment, Watchlist, Bid


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email",)


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_title", "listing_description", "listing_pic", "category", "starting_bid", "current_price", "user", "is_active", "is_closed", "created_time")
    list_editable = ("listing_title", "listing_description", "listing_pic", "category", "starting_bid", "current_price")
    readonly_fields = ("id", "created_time",)
    list_display_links = ("id",)

    def toggle_active(self, request, queryset):
        for listing in queryset:
            listing.is_active = not listing.is_active
            listing.is_closed = not listing.is_closed
            listing.save()

    toggle_active.short_description = "Toggle active status"

    actions = [toggle_active]

class ItemCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "comment")
    list_editable = ("listing", "comment")


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "on_watchlist")


class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "bid", "created_time")


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(ItemComment, ItemCommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
