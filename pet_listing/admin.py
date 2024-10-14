from django.contrib import admin
from .models import Pet, PetImage

class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 5 

class PetAdmin(admin.ModelAdmin):
    inlines = [PetImageInline]
    list_display = ('id', 'name', 'age', 'pet_type', 'breed', 'gender', 'adoption_fee', 'is_available')
    list_filter = ('pet_type', 'breed', 'gender') 
    search_fields = ('name', 'gender', 'breed') 

admin.site.register(Pet, PetAdmin)
