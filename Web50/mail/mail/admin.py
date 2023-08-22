from django.contrib import admin
from .models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "sender", "get_recipients", "subject", "body", "read", "archived")
    list_editable = ("user", "sender", "subject", "body", "read", "archived")

    def get_recipients(self, obj):
        return ", ".join([str(recipient) for recipient in obj.recipients.all()])

admin.site.register(Email, EmailAdmin)