from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as gettext

from rest_framework import serializers
from main_app.models import Documents


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for uploading documents/images"""

    class Meta:
        model = Documents
        fields = ('sigh_number', 'image', 'req_time',
                  'parse_text', 'sig_in_image',)
        read_only_fields = ('sigh_number', 'req_time',
                            'parse_text', 'sig_in_image',)
