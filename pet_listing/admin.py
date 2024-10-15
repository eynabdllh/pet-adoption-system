from django.contrib import admin
from .models import Pet, PetImage

class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1 

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'breed', 'age', 'gender', 'adoption_fee', 'is_available')
    list_filter = ('pet_type', 'is_available', 'gender')
    search_fields = ('name', 'breed')
    list_editable = ('is_available',) 
    inlines = [PetImageInline] 

    fieldsets = (
        (None, {
            'fields': ('name', 'pet_type', 'breed', 'age', 'gender', 'adoption_fee', 'is_available', 'main_image')
        }),
    )

admin.site.register(Pet, PetAdmin)
admin.site.register(PetImage)
