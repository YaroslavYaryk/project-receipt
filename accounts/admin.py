from django.contrib import admin
from .core.admin import BaseAdmin
from django.utils.safestring import mark_safe
from .models import User

# Register your models here.
class UserAdmin(BaseAdmin):

    list_display = (
        "id",
        "email",
        "name",
        "phone",
        "is_active",
        "admin",
    )  # that's will be displayed in django-admin
    list_display_links = ("email",)  # this ones we can click like links
    search_fields = ("email", "name", "phone")
    list_editable = ["is_active"]
    # inlines = [ProductImageAdmin]
    fields = (
        "email",
        "name",
        "phone",
        "address",
        "birthdate",
        "postal_code",
        "city",
        "account_number",
        "is_active",
        "admin",
        "staff",
    )


admin.site.register(User, UserAdmin)
