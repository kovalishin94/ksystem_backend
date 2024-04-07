from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Permission
from . import serializers
from .permissions import IsAdmin, IsMyProfile

class MyPaginator(PageNumberPagination):
    page_size = 10

@api_view(['GET'])
def me(request):
    Profile.objects.filter(id=request.user.profile.id).update(last_seen=timezone.now())
    serializer = serializers.UserMeSerializer(request.user)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdmin])
def user_create(request):
    form = UserCreationForm({
        'username': request.data.get('username'),
        'password1': request.data.get('password1'),
        'password2': request.data.get('password2'),
    })
    if form.is_valid():
        user = form.save()
        try:
            profile = Profile.objects.create(user=user)
            profile_serializer = serializers.ProfileDetailSerializer(profile)

            return Response(profile_serializer.data, status.HTTP_201_CREATED)
        except:
            user.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(form.errors.as_data(), status.HTTP_400_BAD_REQUEST)


class PermissionListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    permission_classes = [IsAdmin]


class ProfileView(ListAPIView):
    serializer_class = serializers.ProfileListSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        queryset = Profile.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(last_name__icontains=search) | 
                Q(first_name__icontains=search) |
                Q(surname__icontains=search)
            )
        return queryset


class ProfileDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileDetailSerializer
    permission_classes = [IsAdmin|IsMyProfile]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.profile.id == instance.id:
            return Response({'message': 'Нельзя удалить свой аккаунт'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.user.delete()

    def update(self, request, *args, **kwargs):
        if not request.user.profile.permissions.filter(name='adm').exists() and 'permissions' in request.data:
            instance_permissions = [permission.id for permission in self.get_object().permissions.all()]
            if not isinstance(request.data.get('permissions'), list):
                return Response({'message': 'Привелегии должны иметь тип список'}, status=status.HTTP_400_BAD_REQUEST)

            if set(instance_permissions) != set(request.data.get('permissions')):
                return Response({'message': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        if request.user.profile.permissions.filter(name='adm').exists() and 'permissions' in request.data:
            if request.user.profile.id == self.get_object().id and 1 not in request.data.get('permissions'):
                return Response({'message': 'Вы не можете снять с себя права администратора'}, status=status.HTTP_403_FORBIDDEN)

        
        return super().update(request, *args, **kwargs)