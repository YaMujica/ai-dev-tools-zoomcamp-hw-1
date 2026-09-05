# Project Plan: Shared Household Chores Tool for Couples

## 1. Overview
A lightweight, low-friction web application designed for couples to manage shared household chores. The tool eliminates nagging and confusion by maintaining a clear view of who is responsible for what, providing an unassigned pool for flexible shared tasks, and fostering positive appreciation with a "Thank You" activity feed.

---

## 2. Target Audience
* **Couples / Small Households** living together who want a simple, transparent, and cooperative way to track everyday chores.

---

## 3. Core Features (Scope)

### Feature 1: Direct Assignment & Shared Unassigned Pool (Grab-Bag)
* Chores can be directly assigned to **Partner A** or **Partner B**.
* Chores can also be left **unassigned** in a shared pool (grab-bag) for flexible, general tasks (e.g., "clean dog poop", "take out trash").
* The dashboard organizes active chores into three clear views: Partner A's chores, Partner B's chores, and the Shared Pool.

### Feature 2: Simple One-Off Checklist Lifecycle
* Tasks follow a straightforward one-off checklist:
  * Users can quickly add a chore with a title and assignment.
  * Tasks remain active until completed.
  * No complex recurring logic or rigid deadlines—keeping everyday usage frictionless.

### Feature 3: One-Click Completion & Claiming
* **For assigned chores**: The assigned partner can mark the task as done with a single click.
* **For shared pool chores**: Either partner can click "Claim & Complete" in a single action, recording that they took care of it.

### Feature 4: Activity Feed with 1-Click "Thank You!" Reactions
* A feed displaying recently completed chores (e.g., *"Alex completed 'Clean dog poop' 15 mins ago"*).
* A 1-click **"Thank You! ❤️"** button next to each completed chore item so partners can acknowledge and appreciate each other's contributions.

---

## 4. Technical Architecture (Django)

* **Framework**: Django 5.x with Python 3.12+ (managed with `uv`)
* **Database**: SQLite (default Django database)
* **Frontend**: Django Templates with clean, responsive CSS
* **Core Data Models**:
  * **Chore**:
    * `title` (CharField): Name/description of the chore.
    * `assigned_to` (CharField/User, nullable): Target partner or None for shared pool.
    * `is_completed` (BooleanField, default False).
    * `completed_by` (CharField/User, nullable): Who completed the task.
    * `completed_at` (DateTimeField, nullable).
    * `created_at` (DateTimeField, auto_now_add=True).
  * **ThankYouReaction**:
    * `chore` (ForeignKey to Chore): The chore being acknowledged.
    * `sender` (CharField/User): Partner who sent the appreciation.
    * `created_at` (DateTimeField, auto_now_add=True).
