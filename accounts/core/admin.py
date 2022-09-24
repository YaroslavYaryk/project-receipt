from django.contrib import admin
from django.utils.safestring import mark_safe


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 200  # max post per page
    list_max_show_all = 50  # max posts after clicking on hyperref
    view_on_site = True
    empty_value_display = ""  # empty one of values

    save_on_top = True
