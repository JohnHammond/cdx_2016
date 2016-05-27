import django.dispatch
key_activated = django.dispatch.Signal(providing_args=["user", "group"])
