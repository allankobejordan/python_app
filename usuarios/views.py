from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .forms import UsuarioForm
from django.contrib import messages


# View para registrar novo usuário
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redireciona pro login após registro
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


# View para listar todos os usuários
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

# @login_required
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso! 🎉')
            return redirect(listar_usuarios)
        else:
             messages.error(request, 'Erro ao cadastrar usuário. Verifique os campos. ❌')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('listar_usuarios')
        else:
            messages.error(request, 'Erro ao atualizar usuário.')
    else:
        form = UsuarioForm(instance=user)

    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': user})           
        
