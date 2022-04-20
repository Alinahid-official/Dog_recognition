from distutils.command.upload import upload
from django.db import models
import os
from django.conf import settings
from django.dispatch import receiver
# Create your models here.
class Dog(models.Model):
    id=models.AutoField(primary_key=True)
    # name=models.CharField(max_length=50,null=True)
    # type=models.CharField( max_length=50,null=True)
    age=models.CharField(max_length=50,null=True)
    breed=models.CharField(max_length=50,null=True)
    size=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='img',null=True)
    
@receiver(models.signals.post_delete, sender=Dog)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            print(instance.image.name)
            # p=os.path.join(settings.STATIC_ROOT,instance.image.name)
            print(settings.STATIC_ROOT)
            # os.remove(p)
            os.remove(instance.image.path)