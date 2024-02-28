from django import forms
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from .models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession
from .forms import WorkoutPlanForm, WorkoutSessionForm
from datetime import timedelta

def home(request):
    return render(request, 'muscleforge/home.html')

class ExerciseListView(ListView):
    model = Exercise
    context_object_name = 'exercises'
    ordering = ['exercise_type']

class ExerciseCreateView(CreateView): # dodati login reguired
    model = Exercise
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        return context

class ExerciseUpdateView(UpdateView): # dodati login reguired
    model = Exercise
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']
    success_url = '/exercises/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        return context

class WorkoutPlanDetailView(DetailView):
    model = WorkoutPlan
    context_object_name = 'workout_plan'

    def get_context_data(self, **kwargs):
        workoutplan = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = f'{workoutplan.title}'
        return context

class WorkoutPlanUpdateView(UpdateView): # dodati login reguired
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    context_object_name = 'workout_plan'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

class WorkoutPlanDeleteView(DeleteView): # dodati login reguired
    model = WorkoutPlan
    success_url = '/workoutplans/'

class WorkoutSessionCreateView(CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        hours = int(self.request.POST.get('hours', 0))
        minutes = int(self.request.POST.get('minutes', 0))
        seconds = int(self.request.POST.get('seconds', 0))
        form.instance.duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        return super().form_valid(form)

    def get_initial(self):
        initial = super(WorkoutSessionCreateView, self).get_initial()
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        if workoutplan_pk:
            initial['workout_plan'] = workoutplan_pk
        return initial

class WorkoutSessionUpdateView(UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        hours = int(self.request.POST.get('hours', 0))
        minutes = int(self.request.POST.get('minutes', 0))
        seconds = int(self.request.POST.get('seconds', 0))
        form.instance.duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        return super().form_valid(form)

class WorkoutSessionDeleteView(DeleteView):
    model = WorkoutSession

    def get_success_url(self):
        workout_plan_id = self.object.workout_plan.id
        return reverse_lazy('workoutplan-detail', kwargs={'pk': workout_plan_id})

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)