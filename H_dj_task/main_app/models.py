from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


def doc_file_path(instance, filename):
    """Generate file path for image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/docs', filename)


class Documents(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # what to do is user is removed
        on_delete=models.SET_NULL,
        null=True
    )
    # filename = models.CharField(max_length=255)
    sigh_number = models.SmallIntegerField(default=0)
    parse_text = models.TextField(blank=True)
    image = models.FileField(upload_to=doc_file_path)
    sig_in_image = models.ImageField(default=None, null=True)
    req_time = models.DateTimeField(auto_now_add=True, editable=True)
    history = HistoricalRecords()

    def __str__(self):
        cur_date = str(self.req_time.strftime('%Y-%m-%d'))
        return self.image.name.split('/')[-1] + " Created =" + cur_date


@receiver(post_delete, sender=Documents)
def submission_delete(sender, instance, **kwargs):
    """Make sure to delete images attached in model"""
    instance.image.delete(False)
    instance.sig_in_image.delete(False)


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in',
                              ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out',
                              ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(
        action='user_login_failed', username=credentials.get('username', None))
