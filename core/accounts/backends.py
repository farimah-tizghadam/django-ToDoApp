from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UsernameEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Allow authentication with both username and email
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        
        if user is not None and user.check_password(password):
            return user
        
        return None