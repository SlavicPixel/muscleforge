from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("workoutplan-detail", kwargs={"pk": self.pk})

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    difficulty_level = models.CharField(max_length=50)
    exercise_type = models.CharField(max_length=50)  
    equipment_needed = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class WorkoutSession(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.DurationField() 
    notes = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("workoutplan-detail", kwargs={"pk": self.workout_plan.pk})

class ExerciseInSession(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField()
    sets = models.IntegerField()
    weight_used = models.FloatField(blank=True, null=True)  

class ProgressTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    body_measurements = models.TextField(blank=True, null=True)  
    notes = models.TextField(blank=True, null=True)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)  
