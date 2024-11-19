from django.db import models
from login_register.models import User
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    message = models.CharField(max_length=200)
    date_sent = models.DateTimeField(default=timezone.now)

    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    
    def get_notifs(user):
        return Notification.objects.filter(user = user)
    
    def get_notifs_filter(user,has_read = True):
        return Notification.objects.filter(user = user, isRead = has_read)
    
    def get_number_of_notifs(user,has_read):
        return Notification.objects.filter(user = user, isRead = has_read).count