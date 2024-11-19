from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from login_register.models import User

# Create your views here.
@login_required
def notification_list(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User,id=user_id)

    notifications = Notification.get_notifs(user)
    unread_count = Notification.get_number_of_notifs(user,False)

    if not user_id:
        return redirect('login')
    
    return render(request, 'notification_list.html',{'notifications': notifications, 'unread_count': unread_count})