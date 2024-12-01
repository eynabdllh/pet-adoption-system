from django.db import models
from django.utils import timezone
from login_register.models import User
from request_form.models import Adoption

# Create your models here.
class NotificationManager(models.Manager):
    def create_for_all_adopters(self, title, message, pet=None):
        adopters = User.objects.filter(isAdmin=False)  # Non-admin users are adopters
        
        notifications = [
            Notification(
                user=adopter,
                title=title,
                message=message,
                pet=pet
            ) for adopter in adopters
        ]
        Notification.objects.bulk_create(notifications)

    def create_for_pet_interactions(self, title, message, pet):
        interacted_users = Adoption.objects.filter(
            pet=pet
        ).values_list('adopter', flat=True).distinct()
        
        notifications = [
            Notification(
                user_id=user_id,
                title=title,
                message=message,
                pet=pet
            ) for user_id in interacted_users
        ]
        Notification.objects.bulk_create(notifications)

    def create_for_adopter(self, adopter, title, message, pet=None):
        return self.create(
            user=adopter,
            title=title,
            message=message,
            pet=pet
        )

    def get_unread_count(self, user):
        return self.filter(user=user, isRead=False).count()

    def get_recent_notifications(self, user, limit=5):
        return self.filter(user=user).order_by('-created_at')[:limit]

    def mark_as_read(self, user, notification_id=None):
        queryset = self.filter(user=user)
        if notification_id:
            queryset = queryset.filter(id=notification_id)
        queryset.update(isRead=True)

    def mark_all_as_read(self, user):
        self.filter(user=user).update(isRead=True)

    def get_pet_notifications(self, user, pet):
        return self.filter(user=user, pet=pet).order_by('-created_at')

    def create_for_all_admins(self, title, message, pet=None):
        admins = User.objects.filter(isAdmin=True)
        
        notifications = [
            Notification(
                user=admin,
                title=title,
                message=message,
                pet=pet
            ) for admin in admins
        ]
        Notification.objects.bulk_create(notifications)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    pet = models.ForeignKey('pet_listing.Pet', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    isRead = models.BooleanField(default=False)

    objects = NotificationManager()

    class Meta:
        ordering = ['-created_at']

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
        return Notification.objects.filter(user = user).count()
    
    def get_number_of_notifs_filter(user,has_read):
        return Notification.objects.filter(user = user, isRead = has_read).count()
    
    def add_notif_to_user(user, title, message):
        try:
            Notification.objects.create(user = user, title = title, message = message)
            return True
        except:
            return False

    def add_notif_to_users_filter(title, message, isAdmin):
        users = User.objects.filter(isAdmin=isAdmin)
        
        try:
            for user in users:
                Notification.add_notif_to_user(user = user, title = title, message = message)
            return True
        except:
            return False
        
    def user_has_unread_notifs(user):
        number_of_notifs = Notification.get_number_of_notifs_filter(user = user,has_read=False)
        if number_of_notifs > 0:
            return True
        else:
            return False