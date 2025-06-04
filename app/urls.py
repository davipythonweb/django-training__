# from django.contrib import admin
# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

# from accounts.views import register_view, login_view, logout_view

# from laptops.views import LaptopsListView, NewlaptopCreateView, LaptopDetailView, LaptopUpdateView, LaptopDeleteView



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
#     path('', LaptopsListView.as_view(), name='laptops_list'),
#     path('new_laptop/', NewlaptopCreateView.as_view(), name='new_laptop'),
#     path('laptop/<int:pk>', LaptopDetailView.as_view(), name='laptop_detail'),
#     path('laptop/<int:pk>/update', LaptopUpdateView.as_view(), name='laptop_update'),
#     path('laptop/<int:pk>/delete', LaptopDeleteView.as_view(), name='laptop_delete'),
# ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) # para configurar uso de armazenar

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('laptops.urls', namespace='laptops')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
