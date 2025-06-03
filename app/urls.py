from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import register_view, login_view, logout_view

from laptops.views import laptopsListView, NewlaptopCreateView, laptopDatailView, laptopUpdateView, laptopDeleteView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', laptopsListView.as_view(), name='laptops_list'),
    path('new_laptop/', NewlaptopCreateView.as_view(), name='new_laptop'),
    path('laptop/<int:pk>', laptopDatailView.as_view(), name='laptop_detail'),
    path('laptop/<int:pk>/update', laptopUpdateView.as_view(), name='laptop_update'),
    path('laptop/<int:pk>/delete', laptopDeleteView.as_view(), name='laptop_delete'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar
