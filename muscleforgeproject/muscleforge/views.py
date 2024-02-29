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
from .models import WorkoutPlan, Exercise, WorkoutSession, ExerciseInSession
from .forms import WorkoutPlanForm, WorkoutSessionForm, ExerciseInSessionFormSet
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

class WorkoutSessionCreateView(WorkoutSessionFormsetMixin, CreateView):
    model = WorkoutSession
    form_class = WorkoutSessionForm

    def get_initial(self):
        initial = super(WorkoutSessionCreateView, self).get_initial()
        workoutplan_pk = self.kwargs.get('workoutplan_pk')
        if workoutplan_pk:
            initial['workout_plan'] = workoutplan_pk
        return initial

class WorkoutSessionUpdateView(WorkoutSessionFormsetMixin, UpdateView):
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

        return context

class WorkoutSessionDeleteView(DeleteView):
    model = WorkoutSession

    def get_success_url(self):
        workout_plan_id = self.object.workout_plan.id
        return reverse_lazy('workoutplan-detail', kwargs={'pk': workout_plan_id})

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)

class WorkoutSessionDetailView(DetailView):
    model = WorkoutSession
    context_object_name = 'workout_session'

    def get_object(self, queryset=None):
        session_pk = self.kwargs.get('session_pk')
        return get_object_or_404(WorkoutSession, pk=session_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Session Details'
        context['exercises'] = ExerciseInSession.objects.filter(workout_session_id=self.kwargs.get('session_pk'))
        return context