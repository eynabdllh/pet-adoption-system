from .models import Notification

def notification_processor(request):
    if request.user.is_authenticated:
        user_id = request.session.get('user_id')
        if user_id:
            unread_count = Notification.get_number_of_notifs_filter(user_id, False)
            recent_notifications = Notification.objects.filter(
                user_id=user_id
            ).order_by('-created_at')[:5]
            
            return {
                'unread_notifications_count': unread_count,
                'recent_notifications': recent_notifications
            }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }

def notifications(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            from login_register.models import User
            user = User.objects.get(id=user_id)
            recent_notifications = Notification.objects.filter(
                user=user
            ).order_by('-created_at')[:5]
            return {
                'notifications': recent_notifications
            }
        except User.DoesNotExist:
            return {'notifications': []}
    return {'notifications': []}