from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from login_register.models import User

@login_required
def notification_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
        base_template = 'base_admin.html' if user.isAdmin else 'base_adopter.html'
        
        if request.method == 'POST':
            if 'mark_all_as_read' in request.POST:
                Notification.objects.filter(user=user).update(isRead=True)
                messages.success(request, 'All notifications marked as read.')
            elif 'remove_all_read' in request.POST:
                Notification.objects.filter(user=user, isRead=True).delete()
                messages.success(request, 'All read notifications have been removed.')
            elif 'remove_notif' in request.POST:
                notif_id = request.POST.get('notif_id')
                Notification.objects.filter(id=notif_id, user=user).delete()
            elif 'mark_as_read' in request.POST:
                notif_id = request.POST.get('notif_id')
                Notification.objects.filter(id=notif_id, user=user).update(isRead=True)
            
            return redirect('notifications')
        
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        
        return render(request, 'notifications/notification_list.html', {
            'notifications': notifications,
            'notif_count': notifications.count(),
            'base_template': base_template
        })
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

@login_required
def mark_as_read(request, notification_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    notification = get_object_or_404(Notification, id=notification_id, user_id=user_id)
    notification.isRead = True
    notification.save()
    return redirect('notifications')

@login_required
def mark_all_as_read(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    Notification.objects.filter(user_id=user_id).update(isRead=True)
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications')

@login_required
def remove_notification(request, notification_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    notification = get_object_or_404(Notification, id=notification_id, user_id=user_id)
    notification.delete()
    return redirect('notifications')

@login_required
def remove_all_read(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    Notification.objects.filter(user_id=user_id, isRead=True).delete()
    messages.success(request, 'All read notifications have been removed.')
    return redirect('notifications') 