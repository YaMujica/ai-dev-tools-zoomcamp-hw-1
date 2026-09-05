from django.db import models
from django.utils import timezone


class Chore(models.Model):
    title = models.CharField(max_length=200)
    assigned_to = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Partner name (e.g. 'Partner A', 'Partner B') or leave empty for Shared Pool",
    )
    is_completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=50, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_completed(self, completed_by=None):
        self.is_completed = True
        self.completed_by = completed_by or self.assigned_to or "Anonymous"
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        assignee = self.assigned_to if self.assigned_to else "Shared Pool"
        status = "Done" if self.is_completed else "Pending"
        return f"{self.title} [{assignee}] - {status}"


class ThankYouReaction(models.Model):
    chore = models.ForeignKey(
        Chore,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    sender = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"❤️ Thank You from {self.sender} on '{self.chore.title}'"
