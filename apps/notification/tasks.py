from celery import shared_task
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.http import JsonResponse, HttpResponse


@shared_task
def send_email(subject, message, to_email):
    """Sending Email in background"""
    if subject and message:
        try:
            email = EmailMessage(
                subject,
                message,
                "renfrid.ngolongolo@sacids.org",
                to_email
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            # response
            return JsonResponse({'error': False, 'message': 'Email sent'})
        except BadHeaderError:
            return JsonResponse({'error': True, 'message': 'Email failed'})
    else:
        return JsonResponse({'error': True, 'message': 'Email failed'})    