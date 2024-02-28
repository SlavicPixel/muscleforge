from django import forms
from django.shortcuts import render
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession
from .forms import WorkoutPlanForm

def home(request):
    return render(request, 'muscleforge/home.html')

class ExerciseListView(ListView):
    model = Exercise
    context_object_name = 'exercises'
    ordering = ['exercise_type']

class ExerciseCreateView(CreateView): # dodati login reguired
    model = Exercise
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']

class ExerciseUpdateView(UpdateView): # dodati login reguired
    model = Exercise
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']
    success_url = '/exercises/'

class ExerciseDeleteView(DeleteView): # dodati login reguired
    model = Exercise
    success_url = '/exercises/'

class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    context_object_name = 'workoutplans'
    ordering = ['start_date']

class WorkoutPlanCreateView(CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = 'workout_plan'