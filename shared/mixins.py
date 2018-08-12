from guardian.mixins import PermissionRequiredMixin
from guardian.utils import get_anonymous_user


class PermissionRequiredMixinWithAnonymous(PermissionRequiredMixin):
    def check_permissions(self, request):
        forbidden = super(PermissionRequiredMixinWithAnonymous, self).check_permissions(request)
        if forbidden:
            perms = self.get_required_permissions(request)
            anon = get_anonymous_user()
            obj = self.get_permission_object()
            has_permissions = all(anon.has_perm(perm, obj) for perm in perms)
            if has_permissions:
                forbidden = None
        return forbidden