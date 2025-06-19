from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, UsuarioForm, CadastroUsuarioForm
from .models import CodigoVerificacao
import random


# Tela pública de registro padrão (antiga, caso ainda use)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado! Faça login.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os campos.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# Tela de cadastro com código de verificação por e-mail
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # aguarda confirmação
            user.username = form.cleaned_data['cpf']  # usando o CPF como username
            user.first_name = form.cleaned_data['nome']
            user.last_name = form.cleaned_data['sobrenome']
            user.save()

            codigo = str(random.randint(100000, 999999))
            CodigoVerificacao.objects.create(user=user, codigo=codigo)

            # Envio do e-mail (padrão console por enquanto)
            send_mail(
                'Seu código de verificação - Street Vibes 90s',
                f'Olá {user.first_name}, seu código de verificação é: {codigo}',
                'no-reply@streetvibes.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Cadastro realizado! Verifique seu e-mail para ativar a conta.')
            return redirect('confirmar_codigo')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os campos obrigatórios.')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})


# Página de confirmação do código de verificação
def confirmar_codigo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        codigo_digitado = request.POST.get('codigo')

        try:
            user = User.objects.get(username=username)
            codigo_obj = CodigoVerificacao.objects.get(user=user)

            if codigo_obj.codigo == codigo_digitado:
                user.is_active = True
                user.save()
                codigo_obj.delete()
                messages.success(request, 'Conta ativada com sucesso! Agora é só fazer o login.')
                return redirect('login')
            else:
                messages.error(request, 'Código incorreto. Tente novamente.')
        except User.DoesNotExist:
            messages.error(request, 'Usuário inválido.')
        except CodigoVerificacao.DoesNotExist:
            # Código não existe? Gera um novo e envia novamente
            codigo_novo = str(random.randint(100000, 999999))
            CodigoVerificacao.objects.create(user=user, codigo=codigo_novo)

            send_mail(
                subject='Novo Código de Verificação - Street Vibes 90s',
                message=f'Fala, {user.first_name}! Seu novo código de verificação é: {codigo_novo}',
                from_email='no-reply@streetvibes.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.warning(request, 'Não encontramos um código válido. Um novo foi enviado para seu e-mail.')
    
    return render(request, 'usuarios/confirmar_codigo.html')
# Listagem de usuários (visível apenas para perfil master)
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


# Edição de usuário
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


# Exclusão de usuário
@login_required
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, 'Usuário excluído com sucesso.')
    return redirect('listar_usuarios')
