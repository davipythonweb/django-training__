
from laptops.models import Laptop
from laptops.forms import laptopModelForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Usando Class Bases Views (Views genericas )  no lugar de (Views Base)=>(Boas Práticas)
class LaptopsListView(ListView):
  model = Laptop
  template_name = 'laptops.html'
  context_object_name = 'laptops'

  def get_queryset(self):
    laptops = super().get_queryset().order_by('model')
    search = self.request.GET.get('search') 
    if search: 
      laptops = laptops.filter(model__icontains=search) 
    return laptops


  
class LaptopDatailView(DetailView):
  model = Laptop
  template_name = 'laptop_detail.html'
  

  
# Usando Class Bases Views (Views genericas )  no lugar de (Views Base)=>(Boas Práticas)
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewlaptopCreateView(CreateView):
  model = Laptop
  form_class = laptopModelForm
  template_name = 'new_laptop.html'
  success_url = '/'
  
  
  
@method_decorator(login_required(login_url='login'), name='dispatch') # decorator para forçar o login para acessar a rota.  
class LaptopUpdateView(UpdateView):
  model = Laptop
  form_class = laptopModelForm
  template_name = 'laptop_update.html'
  
  def get_success_url(self):
    return reverse_lazy('laptop_detail', kwargs={'pk': self.object.pk})
  
  
@method_decorator(login_required(login_url='login'), name='dispatch')  
class LaptopDeleteView(DeleteView):
  model = Laptop
  template_name = 'laptop_delete.html'
  success_url = '/'