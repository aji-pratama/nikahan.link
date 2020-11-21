from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import HomeView, WeddingView


urlpatterns = [
    path('the-dashboard/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('<str:slug>/', WeddingView.as_view(), name='wedding'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
