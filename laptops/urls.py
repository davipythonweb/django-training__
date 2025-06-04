# from django.urls import path
# from .views import laptops
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#   path('', laptops, name='laptops_list'), # um nome para a url, para fazer referência em outras partes
# ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar

from django.urls import path
from . import views

app_name = 'laptops'

urlpatterns = [
    path('', views.LaptopsListView.as_view(), name='laptops_list'),
    path('new/', views.NewLaptopCreateView.as_view(), name='new_laptop'),
    path('<int:pk>/', views.LaptopDetailView.as_view(), name='laptop_detail'),
    path('<int:pk>/update/', views.LaptopUpdateView.as_view(), name='laptop_update'),
    path('<int:pk>/delete/', views.LaptopDeleteView.as_view(), name='laptop_delete'),
]