from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Notification
from login_register.models import User

# Create your views here.
@login_required
def notification_list(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User,id=user_id)

    if not user_id:
        return redirect('login')
    
    if(request.method == 'POST'):
        if 'mark_all_as_read' in request.POST:
            Notification.mark_all_as_read(user)

        elif 'remove_all_read' in request.POST:
            Notification.delete_all_read(user)

        elif 'mark_as_read' in request.POST:
            notif_id = request.POST.get("notif_id")
            Notification.mark_as_read(notif_id)

        elif 'remove_notif' in request.POST:
            notif_id = request.POST.get("notif_id")
            Notification.delete_notif(notif_id)

        return HttpResponseRedirect(reverse("notification_list"))
    
    notifications = Notification.get_notifs(user)
    notif_count = Notification.get_number_of_notifs(user)
    unread_count = Notification.get_number_of_notifs_filter(user,False)
    
    if(user.isAdmin):
        base_template = "base_admin.html"
    else:
        base_template = "base_adopter.html"

    return render(request,'notification_list.html',{'notifications': notifications, 'notif_count': notif_count, 'unread_count': unread_count, 'base_template': base_template})