from Hiragana.models import Stats


def create_user_stats(backend, user, response, *args, **kwargs):
    print('im in user stats')
    if backend.name == 'facebook':
        print('im in backend')
        if user is None:
            Stats.objects.create(user=user)
            print('created stats')
        # profile = user.get_profile()
        # print(profile)
        # profile = Stats.objects.create(user=profile)
        # print(profile)
        # profile.save()
