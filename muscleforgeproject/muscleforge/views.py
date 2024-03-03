from django import forms
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession, Goal
from .forms import WorkoutPlanForm, WorkoutSessionForm, ExerciseInSessionFormSet, GoalForm
from datetime import timedelta

def home(request):
    return render(request, 'muscleforge/home.html')

class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    context_object_name = 'exercises'
    ordering = ['exercise_type']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{'title': 'Exercises'} ]
        context["title"] = 'Exercises'
        return context
    
    
class ExerciseCreateView(LoginRequiredMixin, CreateView): # dodati login reguired
    model = Exercise
    success_url = '/exercises/'
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context["breadcrumbs"] = [{'title': 'Exercises', 'url': reverse_lazy('exercise-list')}, {'title': 'Add Exercise'}]
        context["title"] = 'Add Exercise'
        return context

class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): # dodati login reguired
    model = Exercise
    fields = ['name', 'description', 'difficulty_level', 'exercise_type', 'equipment_needed']
    success_url = '/exercises/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        context["breadcrumbs"] = [{'title': 'Exercises', 'url': reverse_lazy('exercise-list')}, {'title': 'Update Exercise'}]
        context["title"] = 'Update Exercise'
        return context

    def test_func(self):
        exercise = self.get_object()
        if self.request.user.id == exercise.user.id:
            return True
        return False

class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # dodati login reguired
    model = Exercise
    success_url = '/exercises/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{'title': 'Exercises', 'url': reverse_lazy('exercise-list')}, {'title': 'Delete Exercise'}]
        context["title"] = 'Delete Exercise'
        return context

    def test_func(self):
        exercise = self.get_object()
        if self.request.user.id == exercise.user.id:
            return True
        return False

class WorkoutPlanListView(LoginRequiredMixin, ListView):
    model = WorkoutPlan
    context_object_name = 'workoutplans'
    ordering = ['start_date']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{'title': 'Workout Plans'}]
        context["title"] = 'Workout Plans'
        return context

class WorkoutPlanCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        context["breadcrumbs"] = [{'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, {'title': 'Add Workout Plan'}]
        context["title"] = 'Delete Exercise'
        return context

class WorkoutPlanDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkoutPlan
    context_object_name = 'workout_plan'

    def get_context_data(self, **kwargs):
        workoutplan = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, {'title': f'{workoutplan.title}'}]
        context['title'] = f'{workoutplan.title}'
        return context

    def test_func(self):
        workout_plan = self.get_object()
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class WorkoutPlanUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    context_object_name = 'workout_plan'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        workoutplan = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})}, 
            {'title': 'Update'}]
        context['action'] = 'Update'
        return context

    def test_func(self):
        workout_plan = self.get_object()
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class WorkoutPlanDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkoutPlan
    success_url = '/workoutplans/'

    def test_func(self):
        workout_plan = self.get_object()
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

    def get_context_data(self, **kwargs):
        workoutplan = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})}, 
            {'title': 'Delete'}]
        context['action'] = 'Delete'
        return context

class WorkoutSessionFormsetMixin(ModelFormMixin):
    form_class = WorkoutSessionForm
    formset_class = ExerciseInSessionFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Session'
        if self.request.POST:
            context['formset'] = self.formset_class(self.request.POST, instance=self.object)
        else:
            context['formset'] = self.formset_class(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            # This call is necessary to ensure the form's instance is populated with form data.
            self.object = form.save(commit=False)
            self.object.user = self.request.user

            duration_seconds = int(self.request.POST.get('duration', 0))
            self.object.duration = timedelta(seconds=duration_seconds)

            self.object.save()

            formset.instance = self.object
            formset.save()
            return super(ModelFormMixin, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class WorkoutSessionCreateView(LoginRequiredMixin, UserPassesTestMixin, WorkoutSessionFormsetMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm

    def get_context_data(self, **kwargs):
        context = super(WorkoutSessionCreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = ExerciseInSessionFormSet(self.request.POST, self.request.FILES)
        else:
            exercise_formset = ExerciseInSessionFormSet()
            for form in exercise_formset.forms:
                form.fields['exercise'].queryset = Exercise.objects.filter(user=self.request.user)
            context['formset'] = exercise_formset

        workoutplan = get_object_or_404(WorkoutPlan, pk=self.kwargs.get('workoutplan_pk'))
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})}, 
            {'title': 'Add Workout Session'}]

        return context

    def get_initial(self):
        initial = super(WorkoutSessionCreateView, self).get_initial()
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        if workoutplan_pk:
            initial['workout_plan'] = workoutplan_pk
        return initial

    def test_func(self):
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        workout_plan = get_object_or_404(WorkoutPlan, pk=workoutplan_pk)
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class WorkoutSessionUpdateView(LoginRequiredMixin, UserPassesTestMixin, WorkoutSessionFormsetMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)
    
    def get_context_data(self, **kwargs):
        context = super(WorkoutSessionUpdateView, self).get_context_data(**kwargs)
        workout_session = self.get_object()
        duration_seconds = workout_session.duration.total_seconds()

        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        seconds = (duration_seconds % 60)

        context['hours'] = int(hours)
        context['minutes'] = int(minutes)
        context['seconds'] = int(seconds)

        if self.request.method == 'POST':
            context['formset'] = ExerciseInSessionFormSet(self.request.POST, self.request.FILES)
        else:
            exercise_formset = ExerciseInSessionFormSet(instance=workout_session)
            for form in exercise_formset.forms:
                form.fields['exercise'].queryset = Exercise.objects.filter(user=self.request.user)
            context['formset'] = exercise_formset

        workoutplan = get_object_or_404(WorkoutPlan, pk=self.kwargs.get('workoutplan_pk'))
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})},
            {'title': 'Workout Session Details', 'url': reverse_lazy('workoutsession-detail', kwargs={'workoutplan_pk': workoutplan.id, 'session_pk': self.get_object().id})}, 
            {'title': 'Edit Workout Session'}]

        return context
    
    def test_func(self):
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        workout_plan = get_object_or_404(WorkoutPlan, pk=workoutplan_pk)
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class WorkoutSessionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkoutSession

    def get_success_url(self):
        workout_plan_id = self.object.workout_plan.id
        return reverse_lazy('workoutplan-detail', kwargs={'pk': workout_plan_id})

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)
    
    def test_func(self):
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        workout_plan = get_object_or_404(WorkoutPlan, pk=workoutplan_pk)
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workoutplan = get_object_or_404(WorkoutPlan, pk=self.kwargs.get('workoutplan_pk'))
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})},
            {'title': 'Workout Session Details', 'url': reverse_lazy('workoutsession-detail', kwargs={'workoutplan_pk': workoutplan.id, 'session_pk': self.get_object().id})}, 
            {'title': 'Delete Workout Session'}]
        return context
    

class WorkoutSessionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkoutSession
    context_object_name = 'workout_session'

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Session Details'
        context['exercises'] = ExerciseInSession.objects.filter(workout_session_id=self.kwargs.get('session_pk'))
        
        workoutplan = get_object_or_404(WorkoutPlan, pk=self.kwargs.get('workoutplan_pk'))
        context["breadcrumbs"] = [
            {'title': 'Workout Plans', 'url': reverse_lazy('workoutplan-list')}, 
            {'title': f'{workoutplan.title}', 'url': reverse_lazy('workoutplan-detail', kwargs={'pk': workoutplan.id})}, 
            {'title': 'Workout Session Details'}]
        return context
    
    def test_func(self):
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        workout_plan = get_object_or_404(WorkoutPlan, pk=workoutplan_pk)
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    context_object_name = 'goals'
    ordering = ['start_date']

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{'title': 'Goals'} ]
        context["title"] = 'Goals'
        return context

class GoalDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Goal
    context_object_name = 'goal'

    def get_context_data(self, **kwargs):
        workoutplan = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Goals', 'url': reverse_lazy('goal-list')}, 
            {'title': 'Goal Details'}]
        context['title'] = 'Goal Details'
        return context

    def test_func(self):
        workout_plan = self.get_object()
        if self.request.user.id == workout_plan.user.id:
            return True
        return False

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Goals', 'url': reverse_lazy('goal-list')}, 
            {'title': 'Add Goal'}]
        context["title"] = 'Add Goal'
        context["action"] = 'Add'
        return context

class GoalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Goal
    form_class = GoalForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        goal = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Goals', 'url': reverse_lazy('goal-list')}, 
            {'title': 'Goal Details', 'url': reverse_lazy('goal-detail', kwargs={'pk': goal.id})}, 
            {'title': 'Add Goal'}]
        context["title"] = 'Add Goal'
        context["action"] = 'Update'
        return context

    def test_func(self):
        goal = self.get_object()
        if self.request.user.id == goal.user.id:
            return True
        return False

class GoalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Goal
    success_url = '/goals/'

    def get_context_data(self, **kwargs):
        goal = self.get_object()
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {'title': 'Goals', 'url': reverse_lazy('goal-list')}, 
            {'title': 'Goal Details', 'url': reverse_lazy('goal-detail', kwargs={'pk': goal.id})}, 
            {'title': 'Delete Goal'}]
        context["title"] = 'Delete Goal'
        return context
    
    def test_func(self):
        goal = self.get_object()
        if self.request.user.id == goal.user.id:
            return True
        return False


def custom_404(request, exception):
    return render(request, 'muscleforge/404.html', status=404)