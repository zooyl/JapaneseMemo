from Hiragana.models import Stats
from django.contrib.auth.models import User


# def create_user_stats(backend, user, response, *args, **kwargs):
#     print('im in user stats')
#     if backend.name == 'facebook':
#         print('im in backend')
#         if user is None:
#             Stats.objects.create(user=user)
#             print('created stats')
# profile = user.get_profile()
# print(profile)
# profile = Stats.objects.create(user=profile)
# print(profile)
# profile.save()

# def create_user_stats(backend, user, response, *args, **kwargs):
#     if backend.name == 'facebook':
#         profile = user.get_profile()
#         if profile is None:
#             print('none - first time')
#             profile = User.objects.get(user_id=user.id)
#         profile.gender = response.get('gender')
#         profile.link = response.get('link')
#         profile.timezone = response.get('timezone')
#         profile.save()


def create_user_stats(*args, **kwargs):
    ''' check that the user have an existing profile '''
    print('check if user profile exists')
    return Stats.objects.get_or_create(user=kwargs.get('user'))
