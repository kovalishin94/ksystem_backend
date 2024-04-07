from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('security.urls')),
    path('api/chatgpt/', include('chatgpt.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/test/', include('ksystem_test.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
