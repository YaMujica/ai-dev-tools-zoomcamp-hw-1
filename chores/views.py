from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Chore, ThankYouReaction


def dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create":
            title = request.POST.get("title", "").strip()
            assigned_to = request.POST.get("assigned_to", "").strip() or None
            if title:
                Chore.objects.create(title=title, assigned_to=assigned_to)
            return redirect("dashboard")

        elif action == "complete":
            chore_id = request.POST.get("chore_id")
            completed_by = request.POST.get("completed_by", "").strip()
            chore = get_object_or_404(Chore, id=chore_id)
            chore.mark_completed(completed_by=completed_by)
            return redirect("dashboard")

        elif action == "thank_you":
            chore_id = request.POST.get("chore_id")
            sender = request.POST.get("sender", "").strip() or "Partner"
            chore = get_object_or_404(Chore, id=chore_id)
            ThankYouReaction.objects.create(chore=chore, sender=sender)
            return redirect("dashboard")

    partner_a_chores = Chore.objects.filter(is_completed=False, assigned_to="Partner A").order_by("-created_at")
    partner_b_chores = Chore.objects.filter(is_completed=False, assigned_to="Partner B").order_by("-created_at")
    shared_chores = Chore.objects.filter(is_completed=False, assigned_to__isnull=True).order_by("-created_at")
    completed_chores = Chore.objects.filter(is_completed=True).order_by("-completed_at")[:10]

    context = {
        "partner_a_chores": partner_a_chores,
        "partner_b_chores": partner_b_chores,
        "shared_chores": shared_chores,
        "completed_chores": completed_chores,
    }
    return render(request, "chores/index.html", context)
