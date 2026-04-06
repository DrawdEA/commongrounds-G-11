from django.contrib.auth.mixins import AccessMixin

# Assisted by Claude, Prompt: "How to create a custom mixin in Django?" 
class RoleRequiredMixin(AccessMixin):
    """
    You have to set the allowed_role field in your view
    class MyView(RoleRequiredMixin, ListView):
        allowed_role = "A role 
        ...
    """
    allowed_role = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.profile.role != self.allowed_role:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
