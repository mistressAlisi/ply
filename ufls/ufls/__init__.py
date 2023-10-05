
from django.contrib.auth import get_user_model
from .celery import app as celery_app

__all__ = ('celery_app',)

def get_user_by_username_custom(id):
    print(id)
    User = get_user_model()
    user = User.objects.filter(username=id['preferred_username']).first()
    if(user == None):
        user = User.objects.create(username=id['preferred_username'],email=id['email'],first_name=id['given_name'],last_name=id['family_name'], is_staff=True)

    from furry.models import Profile
    profile = Profile.objects.filter(user=user).first()
    if(profile == None):
        profile = Profile.objects.create(user=user, emailMe=True, isStaff=True)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    return user
