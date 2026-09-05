# Project Backlog: Shared Household Chores Tool

Based on [_docs/plan.md](_docs/plan.md), here is the step-by-step implementation backlog:

---

### Task 1: Define Chore & Reaction Models and Run Migrations
* Define the `Chore` model in `chores/models.py` with fields:
  * `title`: CharField(max_length=200)
  * `assigned_to`: CharField(max_length=50, blank=True, null=True) — supports "Partner A", "Partner B", or `None` for shared pool
  * `is_completed`: BooleanField(default=False)
  * `completed_by`: CharField(max_length=50, blank=True, null=True)
  * `completed_at`: DateTimeField(null=True, blank=True)
  * `created_at`: DateTimeField(auto_now_add=True)
* Define the `ThankYouReaction` model:
  * `chore`: ForeignKey(Chore, on_delete=CASCADE, related_name="reactions")
  * `sender`: CharField(max_length=50)
  * `created_at`: DateTimeField(auto_now_add=True)
* Generate and run database migrations (`makemigrations` and `migrate`).

---

### Task 2: Build the Chore Dashboard View and Template
* Create view in `chores/views.py` fetching active chores partitioned into:
  * Partner A's chores
  * Partner B's chores
  * Shared pool (unassigned)
* Create `chores/templates/chores/index.html` with clean, responsive card-based layout.
* Wire up root URLs in `config/urls.py` and `chores/urls.py`.

---

### Task 3: Implement Chore Creation Form
* Add an inline quick-add form at the top of the dashboard:
  * Input for chore title.
  * Dropdown/radio selector for assignment: Partner A, Partner B, or Shared Pool (Unassigned).
* Create view endpoint to handle POST requests, validate input, save the chore, and redirect back.

---

### Task 4: Implement One-Click Completion and Claiming
* Add a POST endpoint `complete_chore(request, chore_id)`:
  * If chore was assigned, marks `is_completed=True`, sets `completed_by` to assignee and `completed_at=timezone.now()`.
  * If chore was in shared pool, allows claiming partner to mark it done as themselves.
* Add 1-click submit buttons on chore cards.

---

### Task 5: Implement Activity Feed with "Thank You" Reaction
* Display recently completed chores at the bottom or side of the dashboard.
* Add a 1-click "Send Thank You! ❤️" button triggering a POST request to create a `ThankYouReaction`.
* Display reaction counter/badges on completed chores in the feed.

---

### Task 6: Write Automated Tests
* Create unit and integration tests in `chores/tests.py`:
  * Testing model creation and default values.
  * Testing chore creation with and without assignment.
  * Testing chore completion and timestamp recording.
  * Testing "Thank You" reaction creation.
