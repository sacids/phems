from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError
from django.http import JsonResponse


# sendEmail
def sendEmail(subject, message, fromEmail, toEmail):
    if subject and message:
        try:
            email = EmailMessage(
                subject,
                message,
                fromEmail,
                toEmail
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            # response
            return JsonResponse({'error': False, 'message': 'Email sent'})
        except BadHeaderError:
            return JsonResponse({'error': True, 'message': 'Email failed'})
    else:
        return JsonResponse({'error': True, 'message': 'Email failed'})