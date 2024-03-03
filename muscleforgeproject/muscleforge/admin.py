from django.contrib import admin
from muscleforge.models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, Goal

model_list = [WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, Goal]

admin.site.register(model_list)
