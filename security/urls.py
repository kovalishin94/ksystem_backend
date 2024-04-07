from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.me, name='me'),
    path('profiles/', views.ProfileView.as_view(), name='profile_list'),
    path('profiles/create/', views.user_create, name='user_create'),
    path('profiles/<uuid:pk>/', views.ProfileDetailUpdateView.as_view(),
         name='profile_get_update_delete'),
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
]
