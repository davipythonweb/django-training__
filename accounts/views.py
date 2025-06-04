# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import authenticate, login, logout


# def register_view(request):
#     if request.method == "POST": # se a requisiçao for post
#         user_form = UserCreationForm(request.POST) # carrega o formulario com os dados
#         if user_form.is_valid(): # verifica se o formulario eh valido
#             user_form.save() # salva
#             return redirect('login') # redireciona para login
#     else:
#         user_form = UserCreationForm() # formulario pronto do django
#     return render(request, 'register.html', {'user_form': user_form})


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username, password=password) # verifica se o usuario e o senha fazem math
#         if user is not None:
#             login(request, user)
#             return redirect('laptops_list') # redireciona para a lista de laptops
#         else:
#             login_form = AuthenticationForm()
#     else:
#         login_form = AuthenticationForm() # carrega o form de login
#     return render(request, 'login.html', {'login_form': login_form})

# def logout_view(request): # fazer logout de sessao
#     logout(request)
#     return redirect('laptops_list')

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, CustomUserChangeForm  # <- Importa o novo form

from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def register_view(request):
    if request.user.is_authenticated:
        return redirect('laptops:laptops_list')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                _('Cadastro realizado com sucesso! Bem-vindo(a), %(username)s!') % 
                {'username': user.username}
            )
            return redirect('laptops:laptops_list')
        messages.error(
            request,
            _('Por favor, corrija os erros abaixo.')
        )
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'title': _('Cadastro de Usuário')
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('laptops:laptops_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    _('Bem-vindo(a) de volta, %(username)s!') % 
                    {'username': user.username}
                )
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('laptops:laptops_list')
        messages.error(
            request,
            _('Login inválido. Por favor, tente novamente.')
        )
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'title': _('Acesso à Conta'),
        'next': request.GET.get('next', '')
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, _('Você foi desconectado com sucesso.'))
        return redirect('laptops:laptops_list')
    return render(request, 'accounts/logout_confirm.html')

@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'title': _('Meu Perfil')
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Perfil atualizado com sucesso.'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('Por favor, corrija os erros abaixo.'))
    else:
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'title': _('Editar Perfil'),
        'is_editing': True  # Para o template saber que é edição
    }
    return render(request, 'accounts/profile.html', context)


@method_decorator(login_required, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, _('Senha alterada com sucesso!'))
        return super().form_valid(form)


# Função auxiliar para proteção de brute force
def handle_brute_force(request):
    failed_logins = request.session.get('failed_logins', 0)
    request.session['failed_logins'] = failed_logins + 1
    if failed_logins > 3:
        messages.warning(
            request,
            _('Muitas tentativas falhas. Tente novamente mais tarde.')
        )
        return True
    return False
