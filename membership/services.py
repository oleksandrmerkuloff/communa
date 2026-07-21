from .models import Membership


def get_membership(user, organization_id):
    return Membership.objects.filter(
        member=user,
        organization_id=organization_id,
    ).first()
