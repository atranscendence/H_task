from django.db import models
import uuid 
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings

def doc_file_path(instance,filename):
    """Generate file path for image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/docs',filename)

class Documents(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # what to do is user is removed
        on_delete=models.SET_NULL,
        null=True
    )
    #filename = models.CharField(max_length=255)
    sigh_number = models.SmallIntegerField(default=0)
    parse_text = models.TextField(blank=True)
    image = models.ImageField(upload_to=doc_file_path)
    req_time = models.DateTimeField(auto_now_add=True,editable=True)


    def __str__(self):
        return self.image.name.split('/')[-1]+" Created ="+str(self.req_time.strftime('%Y-%m-%d'))
