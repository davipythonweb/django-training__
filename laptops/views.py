# from laptops.models import Laptop
# from laptops.forms import LaptopModelForm
# from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator


# # Usando Class Bases Views (Views genericas )  no lugar de (Views Base)=>(Boas Práticas)
# class LaptopsListView(ListView):
#   model = Laptop
#   template_name = 'laptops.html'
#   context_object_name = 'laptops'

#   def get_queryset(self):
#     laptops = super().get_queryset().order_by('model')
#     search = self.request.GET.get('search') 
#     if search: 
#       laptops = laptops.filter(model__icontains=search) 
#     return laptops

# class LaptopDetailView(DetailView):
#   model = Laptop
#   template_name = 'laptop_detail.html'
  
# # Usando Class Bases Views (Views genericas )  no lugar de (Views Base)=>(Boas Práticas)
# @method_decorator(login_required(login_url='login'), name='dispatch')
# class NewlaptopCreateView(CreateView):
#   model = Laptop
#   form_class = LaptopModelForm
#   template_name = 'new_laptop.html'
#   success_url = '/'
  
# @method_decorator(login_required(login_url='login'), name='dispatch') # decorator para forçar o login para acessar a rota.  
# class LaptopUpdateView(UpdateView):
#   model = Laptop
#   form_class = LaptopModelForm
#   template_name = 'laptop_update.html'
  
#   def get_success_url(self):
#     return reverse_lazy('laptop_detail', kwargs={'pk': self.object.pk})
  
# @method_decorator(login_required(login_url='login'), name='dispatch')  
# class LaptopDeleteView(DeleteView):
#   model = Laptop
#   template_name = 'laptop_delete.html'
#   success_url = '/'

from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Laptop
from .forms import LaptopModelForm
import json

class LaptopsListView(ListView):
    model = Laptop
    template_name = 'laptops/laptops.html'
    context_object_name = 'laptops'
    paginate_by = 12  # Paginação com 12 itens por página

    def get_queryset(self):
        queryset = super().get_queryset().select_related('brand').order_by('-id')
        search_term = self.request.GET.get('search')
        
        if search_term:
            queryset = queryset.filter(
                Q(model__icontains=search_term) |
                Q(brand__name__icontains=search_term) |
                Q(cpu__icontains=search_term) |
                Q(gpu__icontains=search_term) |
                Q(ram__icontains=search_term) |
                Q(storage__icontains=search_term)
            )
            messages.info(self.request, f'Resultados para: "{search_term}"')
    
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['featured_laptops'] = Laptop.objects.order_by('-value')[:3]
        context['featured_laptops'] = Laptop.objects.order_by('-price')[:3]
        return context

class LaptopDetailView(DetailView):
    model = Laptop
    template_name = 'laptops/laptop_detail.html'
    context_object_name = 'laptop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_laptops'] = Laptop.objects.filter(
            brand=self.object.brand
        ).exclude(id=self.object.id)[:4]
        return context

class NewLaptopCreateView(LoginRequiredMixin, CreateView):
    model = Laptop
    form_class = LaptopModelForm
    template_name = 'laptops/new_laptop.html'
    success_url = reverse_lazy('laptops:laptops_list')
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        # Adiciona quem cadastrou
        form.instance.added_by = self.request.user

        # Monta o JSON specs a partir dos campos extras do POST
        specs = {
            'cpu': self.request.POST.get('cpu', ''),
            'ram': self.request.POST.get('ram', ''),
            'storage': self.request.POST.get('storage', ''),
            'gpu': self.request.POST.get('gpu', ''),
            'screen': self.request.POST.get('screen', ''),
            'os': self.request.POST.get('os', ''),
            'other': self.request.POST.get('other', ''),
        }
        form.instance.specs = json.dumps(specs, ensure_ascii=False)

        messages.success(self.request, 'Laptop cadastrado com sucesso!')
        return super().form_valid(form)
    

class LaptopUpdateView(LoginRequiredMixin, UpdateView):
    model = Laptop
    form_class = LaptopModelForm
    template_name = 'laptops/laptop_update.html'
    login_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        # Atualiza o JSON specs com os novos valores
        specs = {
            'cpu': self.request.POST.get('cpu', ''),
            'ram': self.request.POST.get('ram', ''),
            'storage': self.request.POST.get('storage', ''),
            'gpu': self.request.POST.get('gpu', ''),
            'screen': self.request.POST.get('screen', ''),
            'os': self.request.POST.get('os', ''),
            'other': self.request.POST.get('other', ''),
        }
        form.instance.specs = json.dumps(specs, ensure_ascii=False)

        messages.success(self.request, 'Laptop atualizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('laptops:laptop_detail', kwargs={'pk': self.object.pk})


class LaptopDeleteView(LoginRequiredMixin, DeleteView):
    model = Laptop
    template_name = 'laptops/laptop_delete.html'
    success_url = reverse_lazy('laptops:laptops_list')
    login_url = reverse_lazy('accounts:login')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Laptop removido com sucesso!')
        return super().delete(request, *args, **kwargs)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)