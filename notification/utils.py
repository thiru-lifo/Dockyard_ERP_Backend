from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from .models import Smtpconfigure

class Util:
    @staticmethod
    def send_email(data):
        try:
            #print('config',config.email_host_user,config.email_host_password)
            config = Smtpconfigure.objects.filter(id=4).first()
            if(config) and config.email_host:
                backend = EmailBackend(
                    host=config.email_host,
                    port=config.email_port,
                    password=config.email_host_password,
                    username=config.email_host_user,
                    use_tls=config.email_use_tls
                )
                email = EmailMultiAlternatives(subject = data['email_subject'], body= data['email_body'], to= [data['to_email']],connection=backend)
                email.attach_alternative(data['email_body'], "text/html")
                email.send()
            else:
                email = EmailMultiAlternatives(subject = data['email_subject'], body= data['email_body'], to= [data['to_email']])
                email.attach_alternative(data['email_body'], "text/html")
                email.send()
            

        except Exception as err:
            print(err)

        
       

    