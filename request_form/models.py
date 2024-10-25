from django.db import models
from pet_listing.models import Pet
from login_register.models import User
from django.utils import timezone

# Create your models here.
class Adoption(models.Model):  # Renamed model
    # Remove any primary_key=True or unique=True on the field
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # This can be non-unique
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField(default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} adopting {self.pet.name}"