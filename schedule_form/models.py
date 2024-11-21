from django.db import models
from pet_listing.models import Pet
from login_register.models import User

# Create your models here.

class Schedule(models.Model):
    REASON_CHOICES = [
        ('duplicate_request', 'Duplicate Request'),
        ('not_picking_up', 'Not Picking Up Pet on Time'),
        ('overwhelmed_adopter', 'Overwhelmed Adopter'),
        ('ethical_safety_concerns', 'Ethical or Safety Concerns'),
        ('inability_to_meet_needs', 'Inability to Meet Pet’s Needs')
    ]
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    month = models.CharField(max_length=20)
    day = models.IntegerField()
    year= models.IntegerField()
    time = models.CharField(max_length=10)
    scheduled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    reason_choices = models.CharField(max_length=50, choices=REASON_CHOICES, null=True)

    def __str__(self):
        return f"Pickup for {self.pet} by {self.adopter} on {self.month} {self.day} {self.year} at {self.time}"
