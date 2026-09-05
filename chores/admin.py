from django.contrib import admin
from .models import Chore, ThankYouReaction


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "is_completed", "completed_by", "completed_at", "created_at")
    list_filter = ("is_completed", "assigned_to")
    search_fields = ("title", "assigned_to", "completed_by")


@admin.register(ThankYouReaction)
class ThankYouReactionAdmin(admin.ModelAdmin):
    list_display = ("chore", "sender", "created_at")
    search_fields = ("chore__title", "sender")
