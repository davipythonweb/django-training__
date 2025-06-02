from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import teste

urlpatterns = [
    path('', teste, name ='teste'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar