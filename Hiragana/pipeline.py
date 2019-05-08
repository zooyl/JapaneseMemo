from Hiragana.models import Stats


def create_user_stats(backend, user, response, *args, **kwargs):
    print('im in user stats')
    if backend.name == 'facebook':
        profile = user.get_profile()
        if profile is None:
            profile = Profile(user_id=user.id)
        profile = Stats.objects.create(user=profile)
        profile.save()
