from django.db import models

class Pet(models.Model):
    PET_TYPE_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('fish', 'Fish'),
        ('bird', 'Bird'),
        ('hamster', 'Hamster'),
        ('rabbit', 'Rabbit'),
        ('guinea_pig', 'Guinea Pig'),
        ('turtle', 'Turtle'),
        ('lizard', 'Lizard'),
        ('snake', 'Snake'),
        ('frog', 'Frog'),
        ('parrot', 'Parrot'),
        ('chinchilla', 'Chinchilla'),
        ('ferret', 'Ferret'),
        ('hedgehog', 'Hedgehog'),
        ('horse', 'Horse'),
        ('goat', 'Goat')
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='pets/main/', null=True, blank=True) 
    time_in_shelter = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.pet_type} ({self.breed})'

class PetImage(models.Model):
    pet = models.ForeignKey(Pet, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets/gallery/', null=True, blank=True)

    def __str__(self):
        return f'{self.pet.name} - Image'