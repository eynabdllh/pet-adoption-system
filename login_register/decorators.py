from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_type') == 'Admin':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view

def adopter_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('user_type') == 'Adopter':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view