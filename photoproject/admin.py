from django.contrib import admin
from .models import Category, Photo, Receipt, Project

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name",)  # that's will be displayed in django-admin
    list_display_links = ("name",)  # this ones we can click like links
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    fields = "name", "slug"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Receipt)
admin.site.register(Photo)
admin.site.register(Project)
