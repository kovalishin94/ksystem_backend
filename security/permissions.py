from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.profile.permissions.filter(name='adm').exists()
        except:
            return False


class IsTestEditor(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.profile.permissions.filter(name='tst').exists()
        except:
            return False


class TestPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            is_editor = request.user.profile.permissions.filter(
                name='tst').exists()
        except:
            return False
        if view.action == 'list' or view.action == 'retrieve':
            return True
        return is_editor


class TestResultPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'retrieve':
            return True
        if view.action == 'list':
            try:
                return request.user.profile.permissions.filter(name='tst').exists()
            except:
                return False
        return False


class IsMyProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            allow = obj.id == request.user.profile.id
        except:
            allow = False
        return allow
