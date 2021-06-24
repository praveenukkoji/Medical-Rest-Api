from user.models import Authorization, View, Role


def can_access(view_name, role_id):
    try:
        view = View.objects.filter(view_name=view_name)[0]
        role = Role.objects.get(pk=role_id)
        authorization = Authorization.objects.filter(view_id=view, role_id=role)
        if len(authorization) > 0:
            return True
        return False
    except Exception as e:
        return False
