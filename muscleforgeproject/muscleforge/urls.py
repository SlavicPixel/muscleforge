from django.urls import path
from . import views
from .views import (
    ExerciseListView,
    ExerciseCreateView,
    ExerciseUpdateView,
    ExerciseDeleteView,
    WorkoutPlanListView,
    WorkoutPlanCreateView,
    WorkoutPlanDetailView
)

urlpatterns = [
    path('', views.home, name="muscleforge-home"),
    path('exercises/', ExerciseListView.as_view(), name="exercise-list"),
    path('exercises/new/', ExerciseCreateView.as_view(), name="exercise-new"),
    path('exercises/<int:pk>/update/', ExerciseUpdateView.as_view(), name="exercise-update"),
    path('exercises/<int:pk>/delete/', ExerciseDeleteView.as_view(), name="exercise-delete"),
    path('workoutplans/', WorkoutPlanListView.as_view(), name="workoutplans-list"),
    path('workoutplans/<int:pk>/', WorkoutPlanDetailView.as_view(), name="workoutplans-detail"),
    path('workoutplans/new/', WorkoutPlanCreateView.as_view(), name="workoutplans-new"),
]
