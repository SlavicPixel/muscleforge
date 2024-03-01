from django.contrib import admin
from muscleforge.models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, ProgressTracker, Goal

model_list = [WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, ProgressTracker, Goal]

admin.site.register(model_list)
