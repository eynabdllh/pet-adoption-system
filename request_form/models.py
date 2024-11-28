from django.db import models
from pet_listing.models import Pet
from login_register.models import User
from profile_management.models import Profile
from django.utils import timezone

class Adoption(models.Model):  
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    REASON_CHOICES = [
        ('duplicate_request', 'Duplicate Request'),
        ('not_picking_up', 'Not Picking Up Pet on Time'),
        ('overwhelmed_adopter', 'Overwhelmed Adopter'),
        ('ethical_safety_concerns', 'Ethical or Safety Concerns'),
        ('inability_to_meet_needs', 'Inability to Meet Pet’s Needs'),
        ('other', 'Other')
    ]

    adopter = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField(default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason_choices = models.CharField(max_length=50, choices=REASON_CHOICES, default='other', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} wants to adopt {self.pet.name}"