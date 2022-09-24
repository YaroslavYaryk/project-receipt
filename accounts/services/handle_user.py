from accounts.models import User


def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except Exception:
        return None


def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except Exception:
        return None


def get_all_workers(user):
    return User.objects.exclude(id=user.id)
