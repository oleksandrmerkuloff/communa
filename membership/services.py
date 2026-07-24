from django.contrib.auth.models import AnonymousUser

from .models import Membership


def get_membership(user, organization_id):
    if not user or not user.is_authenticated:
        return None

    return Membership.objects.filter(
        member=user,
        organization_id=organization_id,
    ).first()
