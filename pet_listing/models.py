from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    pet_type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    main_image = models.ImageField(upload_to='pets/', blank=True, null=True)

    def __str__(self):
        return self.name

class PetImage(models.Model):
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets/')

    def __str__(self):
        return f"{self.pet.name} Image"
