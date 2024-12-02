from django.contrib import admin
from .models import Pet, PetImage

admin.site.register(Pet)
admin.site.register(PetImage)