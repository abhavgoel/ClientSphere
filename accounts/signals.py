#here we create signals so that whenever a new user is registered, we can create it as a customer too
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import Customer

def customer_profile(sender,instance,created, **kwargs):
    if created:
        group,created = Group.objects.get_or_create(name='customer')
        instance.groups.add(group)

        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
post_save.connect(customer_profile,sender=User)