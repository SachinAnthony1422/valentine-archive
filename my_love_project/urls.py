from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from valentine import views  # 👈 Add this line!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('valentine.urls')),
    path('promise/', views.promise, name='promise'),
]

# This allows us to serve BOTH Media (Uploads) and Static (Design Files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 👇 THIS IS THE NEW LINE YOU NEED!
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')