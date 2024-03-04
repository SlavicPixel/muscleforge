from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from muscleforge.models import Exercise, WorkoutPlan, WorkoutSession, Goal
from datetime import date, timedelta

# Checking if the ExerciseListView correctly returns exercises for the logged-in user
class ExerciseListViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        # Create some exercises for this user
        Exercise.objects.create(name="Push Up", user=self.user)
        Exercise.objects.create(name="Pull Up", user=self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/exercises/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('exercise-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'muscleforge/exercise_list.html')

    def test_lists_only_user_exercises(self):
        # Create another user and exercise not to be seen by the original user
        other_user = User.objects.create_user(username='otheruser', password='12345')
        Exercise.objects.create(name="Squat", user=other_user)

        response = self.client.get(reverse('exercise-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('exercises' in response.context)
        self.assertEqual(len(response.context['exercises']), 13)
        self.assertEqual(response.context['exercises'][0].user, self.user)
        self.assertEqual(response.context['exercises'][1].user, self.user)

# Ensuring that ExerciseCreateView correctly creates an exercise for the logged-in user
class ExerciseCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/exercises/new/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('exercise-new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'muscleforge/exercise_form.html')

    def test_can_save_a_POST_request(self):
        self.client.post(reverse('exercise-new'), data={
            'name': 'New Exercise',
            'description': 'Test Description',
            'difficulty_level': 'Beginner',
            'exercise_type': 'Cardio',
            'equipment_needed': 'None',
        })
        self.assertEqual(Exercise.objects.count(), 12) 
        new_exercise = Exercise.objects.filter(name='New Exercise').first()
        self.assertEqual(new_exercise.name, 'New Exercise')
        self.assertEqual(new_exercise.user, self.user)

# Ensuring that WorkoutPlanDetailView works as expected for the logged-in user and that it correctly restricts access based on ownership
# Add to your tests/test_views.py

class WorkoutPlanDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='test123')
        self.other_user = User.objects.create_user(username='user2', password='test123')
        self.workout_plan = WorkoutPlan.objects.create(title="Plan 1", start_date=date.today(), end_date=date.today() + timedelta(days=10), user=self.user)

    def test_user_can_access_own_workout_plan_detail(self):
        self.client.login(username='user1', password='test123')
        response = self.client.get(reverse('workoutplan-detail', kwargs={'pk': self.workout_plan.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.workout_plan.title)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('workoutplan-detail', kwargs={'pk': self.workout_plan.pk}))
        self.assertRedirects(response, f"/login/?next=/workoutplans/{self.workout_plan.pk}/")

    def test_user_cannot_access_other_users_workout_plan_detail(self):
        self.client.login(username='user2', password='test123')
        response = self.client.get(reverse('workoutplan-detail', kwargs={'pk': self.workout_plan.pk}))
        self.assertEqual(response.status_code, 403)

# Check if WorkoutPlanUpdateView only allows access to the owner of the plan and that it successfully updates the plan's data
class WorkoutPlanUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='test123')
        self.workout_plan = WorkoutPlan.objects.create(title="Original Title", start_date=date.today(), end_date=date.today() + timedelta(days=10), user=self.user)
        self.client.login(username='user1', password='test123')

    def test_user_can_update_own_workout_plan(self):
        response = self.client.post(reverse('workoutplan-update', kwargs={'pk': self.workout_plan.pk}), {
            'title': 'Updated Title',
            'start_date': self.workout_plan.start_date,
            'end_date': self.workout_plan.end_date,
        })
        self.workout_plan.refresh_from_db()
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(self.workout_plan.title, 'Updated Title')

    def test_user_cannot_update_other_users_workout_plan(self):
        other_user = User.objects.create_user(username='user2', password='test123')
        self.client.login(username='user2', password='test123')
        response = self.client.post(reverse('workoutplan-update', kwargs={'pk': self.workout_plan.pk}), {})
        self.assertEqual(response.status_code, 403)

# Checks if the GoalListView correctly returns only the goals for the logged-in user, ensuring user data is properly isolated
class GoalListViewTest(TestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='test123')
        self.user2 = User.objects.create_user(username='user2', password='test12345')

        # Create goals for each user
        Goal.objects.create(title="User 1 Goal", user=self.user1, start_date=date.today(), end_date=date.today() + timedelta(days=10))
        Goal.objects.create(title="User 2 Goal", user=self.user2, start_date=date.today(), end_date=date.today() + timedelta(days=5))

        # Log in as user1
        self.client.login(username='user1', password='test123')

    def test_lists_only_user_goals(self):
        response = self.client.get(reverse('goal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('goals' in response.context)
        self.assertEqual(len(response.context['goals']), 1)
        self.assertEqual(response.context['goals'][0].user, self.user1)
        self.assertEqual(response.context['goals'][0].title, "User 1 Goal")

