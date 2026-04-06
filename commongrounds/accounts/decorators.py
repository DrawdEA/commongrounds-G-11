from functools import wraps
from django.http import HttpResponseForbidden

# Assisted by Claude, Prompt: "How to create a custom decorator in Django?" 
def role_required(allowed_role):
    """
    Use like this
    @role_required("A Role")
    def my_view(request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.shortcuts import redirect
                return redirect('accounts:login')
            if request.user.profile.role != allowed_role:
                return HttpResponseForbidden("You don't have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
