from django.contrib.auth import get_user_model


def get_user_by_username(id):
	User = get_user_model()
	user, created = User.objects.get_or_create(username=id['sub'])
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	return user
