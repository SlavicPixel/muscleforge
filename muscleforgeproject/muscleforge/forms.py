from django import forms
from django.forms import inlineformset_factory
from .models import WorkoutPlan, WorkoutSession, ExerciseInSession, Goal

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['title', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['workout_plan', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExerciseInSessionForm(forms.ModelForm):
    class Meta:
        model = ExerciseInSession
        fields = ['exercise', 'repetitions', 'sets', 'weight_used'] #excluded durations

ExerciseInSessionFormSet = inlineformset_factory(
    WorkoutSession, ExerciseInSession, form=ExerciseInSessionForm,
    extra=1, can_delete=True, can_delete_extra=True
)

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'start_date', 'end_date', 'description', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
