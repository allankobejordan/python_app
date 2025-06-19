from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CadastroUsuarioForm
from .models import CodigoVerificacao, PerfilUsuario
from django.http import HttpResponse
import random

def cadastrar_usuario(request):
    user_logado = request.user if request.user.is_authenticated else None

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST, user_logado=user_logado)
        if form.is_valid():
            user = form.save(commit=False)

            if user_logado and user_logado.perfilusuario.perfil == 'master':
                user.is_active = True
                user.save()

                PerfilUsuario.objects.create(
                    user=user,
                    telefone=form.cleaned_data['telefone'],
                    cpf=form.cleaned_data['cpf'],
                    perfil=form.cleaned_data.get('perfil', 'comum')
                )

                messages.success(request, 'Usuário criado com sucesso!')
                return redirect('listar_usuarios')
            else:
                user.is_active = False
                user.save()

                PerfilUsuario.objects.create(
                    user=user,
                    telefone=form.cleaned_data['telefone'],
                    cpf=form.cleaned_data['cpf'],
                    perfil='comum'
                )

                codigo = str(random.randint(100000, 999999))
                CodigoVerificacao.objects.create(user=user, codigo=codigo)

                send_mail(
                    subject='Código de verificação - Street Vibes 90s',
                    message=f'E aí, {user.first_name}! Seu código: {codigo}',
                    from_email='no-reply@streetvibes.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Cadastro salvo! Verifique seu e-mail com o código.')
                return redirect('confirmar_codigo')
    else:
        form = CadastroUsuarioForm(user_logado=user_logado)

    return render(request, 'usuarios/cadastrar_usuario.html', {'form': form})

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
                messages.success(request, 'Conta ativada com sucesso! Agora é só fazer login.')
                return redirect('login')
            else:
                messages.error(request, 'Código incorreto.')
        except:
            messages.error(request, 'Usuário ou código inválido.')

    return render(request, 'usuarios/confirmar_codigo.html')

@login_required
def listar_usuarios(request):
    try:
        if request.user.perfilusuario.perfil != 'master':
            messages.error(request, 'Você não tem permissão para acessar essa página.')
            return redirect('home')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')

    usuarios = User.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado!')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=user)

    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': user})

@login_required
def excluir_usuario(request, id):
    usuario = get_object_or_404(User, pk=id)
    usuario.delete()
    messages.success(request, 'Usuário excluído com sucesso.')
    return redirect('listar_usuarios')

def send_test_email(request):
    assunto = 'E-mail de Teste - Street Vibes 90s'
    mensagem = 'Se você está lendo isso, o envio de e-mail está funcionando! 🎉'
    remetente = 'allanjordan2011@gmail.com'
    destino = ['allanjordan2011@gmail.com']

    try:
        send_mail(assunto, mensagem, remetente, destino)
        return HttpResponse("✅ E-mail enviado com sucesso!")
    except Exception as e:
        return HttpResponse(f"❌ Erro ao enviar e-mail: {e}")
