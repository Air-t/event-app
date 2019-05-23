from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


def is_in_owner_group(user):
    """Check if logged user is in owner Group"""
    if user.is_anonymous:
        return False
    return user.is_owner


class LoginRequiredOwnerMixin(AccessMixin):
    """Mixin to validate if currently logged user is in owner group"""
    def get_login_url(self):
        if self.request.user:
            return super(LoginRequiredOwnerMixin, self).get_login_url()
        return redirect('events:home')

    def test_func(self):
        return is_in_owner_group(self.request.user)
