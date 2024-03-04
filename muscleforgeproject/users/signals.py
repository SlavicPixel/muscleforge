from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
from muscleforge.models import Exercise

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=User)
def create_default_exercises_for_new_user(sender, instance, created, **kwargs):
    if created:
        default_exercises = [
            {'name': 'Push-up', 'description': 'Perform a high plank position and lower your body until your chest touches the floor. Push back up.', 'difficulty_level': 'Beginner', 'exercise_type': 'Strength', 'equipment_needed': 'None'},
            {'name': 'Sit-up', 'description': 'Lie on your back, bend your knees and lift your torso towards your knees.', 'difficulty_level': 'Beginner', 'exercise_type': 'Core', 'equipment_needed': 'None'},
            {'name': 'Pull-up', 'description': 'Hang from a bar with your hands shoulder-width apart and pull yourself up until your chin passes the bar.', 'difficulty_level': 'Intermediate', 'exercise_type': 'Strength', 'equipment_needed': 'Pull-up Bar'},
            {'name': 'Squats', 'description': 'Stand with feet a little wider than shoulder-width apart, hips stacked over knees, and knees over ankles. Lower down as if sitting into a chair.', 'difficulty_level': 'Beginner', 'exercise_type': 'Legs', 'equipment_needed': 'None'},
            {'name': 'Lunges', 'description': 'Step forward with one leg, lowering your hips until both knees are bent at about a 90-degree angle.', 'difficulty_level': 'Beginner', 'exercise_type': 'Legs', 'equipment_needed': 'None'},
            {'name': 'Plank', 'description': 'Hold a push-up position, with your body weight borne on your arms, elbows, and toes. Maintain a straight back.', 'difficulty_level': 'Beginner', 'exercise_type': 'Core', 'equipment_needed': 'None'},
            {'name': 'Burpees', 'description': 'Start in a standing position, drop into a squat with your hands on the ground, then kick your feet back while keeping your arms extended. Immediately return your feet to the squat position and jump up.', 'difficulty_level': 'Advanced', 'exercise_type': 'Cardio', 'equipment_needed': 'None'},
            {'name': 'Deadlift', 'description': 'Bend and lift the weight with your legs while keeping your back straight.', 'difficulty_level': 'Intermediate', 'exercise_type': 'Strength', 'equipment_needed': 'Barbell'},
            {'name': 'Bench Press', 'description': 'Lie back on a bench and push a weight away from your chest.', 'difficulty_level': 'Intermediate', 'exercise_type': 'Strength', 'equipment_needed': 'Bench, Barbell'},
            {'name': 'Bicep Curl', 'description': 'Hold a weight in your hands and, with elbows fixed, curl the weight towards your shoulder.', 'difficulty_level': 'Beginner', 'exercise_type': 'Arms', 'equipment_needed': 'Dumbbell'},
            {'name': 'Tricep Dip', 'description': 'On a chair or bench, support your body with your arms and lower yourself until your elbows are bent between 45 and 90 degrees. Extend your elbows to return to the starting position.', 'difficulty_level': 'Intermediate', 'exercise_type': 'Arms', 'equipment_needed': 'Chair or Bench'},
        ]

        for exercise in default_exercises:
            Exercise.objects.create(user=instance, **exercise)