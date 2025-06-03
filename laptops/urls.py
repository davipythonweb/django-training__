from django.urls import path
from .views import laptops
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', laptops, name='laptops_list'), # um nome para a url, para fazer referência em outras partes
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar

