from django.contrib import admin# sala@gmail.com sala
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('collect_data.urls')),
    path('wish_list/', include('wish_list.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

