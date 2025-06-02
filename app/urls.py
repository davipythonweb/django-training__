from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from laptops.views import current_datetime

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teste/', current_datetime, name='teste'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar
