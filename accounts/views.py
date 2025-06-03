from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == "POST": # se a requisiçao for post
        user_form = UserCreationForm(request.POST) # carrega o formulario com os dados
        if user_form.is_valid(): # verifica se o formulario eh valido
            user_form.save() # salva
            return redirect('login') # redireciona para login
    else:
        user_form = UserCreationForm() # formulario pronto do django
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) # verifica se o usuario e o senha fazem math
        if user is not None:
            login(request, user)
            return redirect('laptops_list') # redireciona para a lista de laptops
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm() # carrega o form de login
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request): # fazer logout de sessao
    logout(request)
    return redirect('laptops_list')