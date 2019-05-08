from Hiragana.models import Stats


def create_user_stats(*args, **kwargs):
    """
    create stats for user if he already doesn't have one
    """
    Stats.objects.get_or_create(user=kwargs.get('user'))
