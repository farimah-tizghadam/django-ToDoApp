from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    empty_value_display = "unknown"
    list_display = ["title", "user", "complete", "creation_date"]
    list_filter = ("complete", "user")
    search_fields = ["title"]
    pass


admin.site.register(Task, TaskAdmin)
