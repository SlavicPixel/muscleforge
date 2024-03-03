from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    ExerciseListView,
    ExerciseCreateView,
    ExerciseUpdateView,
    ExerciseDeleteView,
    WorkoutPlanListView,
    WorkoutPlanCreateView,
    WorkoutPlanDetailView,
    WorkoutPlanUpdateView,
    WorkoutPlanDeleteView,
    WorkoutSessionCreateView,
    WorkoutSessionDetailView,
    WorkoutSessionUpdateView,
    WorkoutSessionDeleteView,
    GoalListView,
    GoalDetailView,
    GoalCreateView,
    GoalUpdateView,
    GoalDeleteView
)

urlpatterns = [
    path('', views.home, name="muscleforge-home"),
    path('exercises/', ExerciseListView.as_view(), name="exercise-list"),
    path('exercises/new/', ExerciseCreateView.as_view(), name="exercise-new"),
    path('exercises/<int:pk>/update/', ExerciseUpdateView.as_view(), name="exercise-update"),
    path('exercises/<int:pk>/delete/', ExerciseDeleteView.as_view(), name="exercise-delete"),
    path('workoutplans/', WorkoutPlanListView.as_view(), name="workoutplan-list"),
    path('workoutplans/<int:pk>/', WorkoutPlanDetailView.as_view(), name="workoutplan-detail"),
    path('workoutplans/new/', WorkoutPlanCreateView.as_view(), name="workoutplan-new"),
    path('workoutplans/<int:pk>/update/', WorkoutPlanUpdateView.as_view(), name="workoutplan-update"),
    path('workoutplans/<int:pk>/delete/', WorkoutPlanDeleteView.as_view(), name="workoutplan-delete"),
    path('workoutplans/<int:workoutplan_pk>/workoutsession/new', WorkoutSessionCreateView.as_view(), name="workoutsession-new"),
    path('workoutplans/<int:workoutplan_pk>/workoutsession/<int:session_pk>/', WorkoutSessionDetailView.as_view(), name="workoutsession-detail"),
    path('workoutplans/<int:workoutplan_pk>/workoutsession/<int:session_pk>/update', WorkoutSessionUpdateView.as_view(), name="workoutsession-update"),
    path('workoutplans/<int:workoutplan_pk>/workoutsession/<int:session_pk>/delete', WorkoutSessionDeleteView.as_view(), name="workoutsession-delete"),
    path('goals/', GoalListView.as_view(), name="goal-list"),
    path('goals/new', GoalCreateView.as_view(), name="goal-new"),
    path('goals/<int:pk>/', GoalDetailView.as_view(), name="goal-detail"),
    path('goals/<int:pk>/update/', GoalUpdateView.as_view(), name="goal-update"),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name="goal-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)