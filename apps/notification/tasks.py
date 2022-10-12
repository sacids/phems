from celery import shared_task


@shared_task
def notification():
    for _ in range(10):
        print('it is running')
    return 'Done !'