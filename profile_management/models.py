from django.db import models
from login_register.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save_profile(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.user.save()

    def clean(self):
        if self.age is not None and self.age < 0:
            raise ValidationError('Age cannot be negative.')
        
    def update_profile_image(self, image):
        self.profile_image = image
        self.save()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()