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
    # --- 🎆 THE GRAND FINALE (VALENTINE'S DAY) 🎆 ---
    path('valentine-start/', views.valentine_start, name='valentine_start'),
    path('valentine-game/', views.valentine_game, name='valentine_game'),
    path('valentine-quiz/', views.valentine_quiz, name='valentine_quiz'),
    path('valentine-doors/', views.valentine_doors, name='valentine_doors'),
    path('valentine-teddy/', views.valentine_teddy, name='valentine_teddy'),
    path('valentine-gallery/', views.valentine_gallery, name='valentine_gallery'),
    path('valentine-finale/', views.valentine_finale, name='valentine_finale'),
]

# This allows us to serve BOTH Media (Uploads) and Static (Design Files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 👇 THIS IS THE NEW LINE YOU NEED!
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')