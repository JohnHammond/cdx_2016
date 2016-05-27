import django.dispatch

new_user_created = django.dispatch.Signal(providing_args=['user'])
