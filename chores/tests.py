from django.test import TestCase, Client
from django.urls import reverse
from .models import Chore, ThankYouReaction


class ChoreModelTests(TestCase):
    def test_create_assigned_chore(self):
        chore = Chore.objects.create(title="Do the dishes", assigned_to="Partner A")
        self.assertEqual(chore.title, "Do the dishes")
        self.assertEqual(chore.assigned_to, "Partner A")
        self.assertFalse(chore.is_completed)
        self.assertIsNone(chore.completed_at)

    def test_create_shared_pool_chore(self):
        chore = Chore.objects.create(title="Clean dog poop", assigned_to=None)
        self.assertIsNone(chore.assigned_to)
        self.assertIn("Shared Pool", str(chore))

    def test_mark_completed_method(self):
        chore = Chore.objects.create(title="Fold laundry", assigned_to="Partner B")
        chore.mark_completed(completed_by="Partner B")
        self.assertTrue(chore.is_completed)
        self.assertEqual(chore.completed_by, "Partner B")
        self.assertIsNotNone(chore.completed_at)

    def test_thank_you_reaction(self):
        chore = Chore.objects.create(title="Vacuum living room", is_completed=True)
        reaction = ThankYouReaction.objects.create(chore=chore, sender="Partner A")
        self.assertEqual(reaction.chore, chore)
        self.assertEqual(chore.reactions.count(), 1)


class ChoreDashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse("dashboard")

    def test_dashboard_get(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ChoreHarmony")

    def test_create_chore_via_post(self):
        response = self.client.post(self.dashboard_url, {
            "action": "create",
            "title": "Mow the lawn",
            "assigned_to": "Partner A",
        })
        self.assertEqual(response.status_code, 302)
        chore = Chore.objects.get(title="Mow the lawn")
        self.assertEqual(chore.assigned_to, "Partner A")

    def test_complete_chore_via_post(self):
        chore = Chore.objects.create(title="Take out recycling", assigned_to=None)
        response = self.client.post(self.dashboard_url, {
            "action": "complete",
            "chore_id": chore.id,
            "completed_by": "Partner B",
        })
        self.assertEqual(response.status_code, 302)
        chore.refresh_from_db()
        self.assertTrue(chore.is_completed)
        self.assertEqual(chore.completed_by, "Partner B")

    def test_send_thank_you_via_post(self):
        chore = Chore.objects.create(title="Water plants", is_completed=True)
        response = self.client.post(self.dashboard_url, {
            "action": "thank_you",
            "chore_id": chore.id,
            "sender": "Partner A",
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(chore.reactions.count(), 1)
