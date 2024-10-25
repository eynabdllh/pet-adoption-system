from django.db import models
from pet_listing.models import Pet
from login_register.models import User

# Create your models here.

class Schedule(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Use ForeignKey to reference Adoption
    month = models.CharField(max_length=20)
    day = models.IntegerField()
    year= models.IntegerField()
    time = models.CharField(max_length=10)
    scheduled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pickup for {self.pet} by {self.adopter} on {self.month} {self.day} at {self.time}"
