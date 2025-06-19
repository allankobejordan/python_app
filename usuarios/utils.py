from django.core.mail import send_mail
from django.conf import settings

def enviar_email_confirmacao(email_destino, codigo):
    assunto = 'Confirmação de Cadastro - Street Vibes 90s'
    mensagem = f'''
    Olá!

    Seu código de verificação do sistema *Street Vibes 90s* é:

    👉 CÓDIGO: {codigo}

    Copie e cole esse código para confirmar seu cadastro e liberar o acesso.

    Se você não solicitou esse cadastro, apenas ignore este e-mail.

    Atenciosamente,  
    Equipe Street Vibes 90s
    '''
    remetente = settings.DEFAULT_FROM_EMAIL  # Usa o que tá no settings.py

    try:
        send_mail(
            assunto,
            mensagem,
            remetente,
            [email_destino],
            fail_silently=False,
        )
        print(f"✅ E-mail de verificação enviado para: {email_destino}")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail para {email_destino}: {e}")
