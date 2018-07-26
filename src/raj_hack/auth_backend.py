from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from model_utils.managers import InheritanceQuerySet


class CustomUserModelBackend(ModelBackend):
    def get_user(self, user_id):
        try:

        	return InheritanceQuerySet(User).select_subclasses().get(pk=user_id)
        except User.DoesNotExist:
        	return None


    def authenticate(self, request, username=None, password=None):
        try:
            user = InheritanceQuerySet(User).select_subclasses().get(username=username, password=password)
            return user
        except User.DoesNotExist:
            print('User Does Not Found')
            return None
