from celery import shared_task


@shared_task
def notification():
    for _ in range(10):
        print('it is running')
    return 'Done !'


@shared_task
def send_email(subject, message, from_email, to_email):
    if subject and message:
        try:
            email = EmailMessage(
                subject,
                message,
                from_email,
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