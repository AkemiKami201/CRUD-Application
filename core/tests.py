from config.wsgi import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from core.user.models import User


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'email'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_TO = 'address'


def send_email():
    try:
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        print('Conectado...')

        mensaje = MIMEMultipart(""" Este es un nuevo mensaje de Prueba""")
        mensaje['From'] = EMAIL_HOST_USER
        mensaje['To'] = EMAIL_TO
        mensaje['Subject'] = "Tienes un nuevo correo"

        content = render_to_string('send_email.html', {'user': User.objects.get(pk=1)})
        mensaje.attach(MIMEText(content, 'html'))
        mailServer.sendmail(EMAIL_HOST_USER, EMAIL_TO, mensaje.as_string())

        print("Correo enviado")
    except Exception as e:
        print(e)


send_email()
