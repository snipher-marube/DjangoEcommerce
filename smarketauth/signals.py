from django.contrib.auth.models import User
from django.db.models.signals import pre_save

def update_username(sender, instance, **kwargs):
    instance.username = instance.email
pre_save.connect(update_username, sender=User)
