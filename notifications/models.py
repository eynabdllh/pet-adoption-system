from django.db import models
from login_register.models import User
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="Unnamed Title")
    message = models.CharField(max_length=400, default="No message attached")
    date_sent = models.DateTimeField(default=timezone.now)

    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    
    #for marking all non read
    def mark_all_as_read(user):
        return Notification.objects.filter(user = user, isRead = False).order_by('-date_sent').update(isRead = True)
    
    #for deleting all read
    def delete_all_read(user):
        return Notification.objects.filter(user = user, isRead = True).delete()
    
    #mark one notif as read
    def mark_as_read(notif_id):
        return Notification.objects.filter(id = notif_id).update(isRead = True)
    
    #delete one notif
    def delete_notif(notif_id):
        return Notification.objects.filter(id = notif_id).delete()

    #get user notifs by latest order
    def get_notifs(user):
        return Notification.objects.filter(user = user).order_by('-date_sent')
    
    def get_notifs_filter(user,has_read = True):
        return Notification.objects.filter(user = user, isRead = has_read).order_by('-date_sent')
    
    def get_number_of_notifs(user):
        return Notification.objects.filter(user = user).count
    
    def get_number_of_notifs_filter(user,has_read):
        return Notification.objects.filter(user = user, isRead = has_read).count