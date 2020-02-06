# Django
from django.conf import settings
from django.urls import reverse #retorna string

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives



class Mail:

    @staticmethod
    def get_absolut_url(url):
        if settings.DEBUG: #En modo desarrollo
            return 'http://127.0.0.1:8000{}'.format(
                reverse(url)
            )

    @staticmethod
    def send_complete_order(order, user):
        subject = 'Tu pedido ha sido enviado'
        template = get_template('orders/mails/complete.html')

        content = template.render({
            'user': user,
            'next_url': Mail.get_absolut_url('orders:completeds')
        })

        message = EmailMultiAlternatives(subject,
                                        'Mensaje importante',
                                        settings.EMAIL_HOST_USER,
                                        [user.email])

        message.attach_alternative(content, 'text/html')
        message.send()