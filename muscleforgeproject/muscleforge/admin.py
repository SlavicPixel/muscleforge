from django.contrib import admin
from muscleforge.models import UserProfile, WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, ProgressTracker, Goal

model_list = [UserProfile, WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, ProgressTracker, Goal]

admin.site.register(model_list)
