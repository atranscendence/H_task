from django.shortcuts import render

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Documents
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api_app import serializers
from rest_framework import viewsets, mixins
from api_app.image_parsing import img_parse_main


class DocumentsViewSet(viewsets.ModelViewSet):
    """Manage documents in the database"""
    http_method_names = ['get', 'post']
    serializer_class = serializers.DocumentSerializer
    queryset = Documents.objects.all()

    # Enable token authentication
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request):
        doc = request.data
        doc_type = request.query_params.get('doc_type', 'Advanced')

        serializer = self.get_serializer(data=doc)

        if serializer.is_valid():
            valid_formats = ['jpg', 'png', 'pdf']
            img_format = doc['image'].name.split('.')[-1]
            if (img_format in valid_formats):
                obj = serializer.save(user=self.request.user)

                return img_parse_main.get_sights(obj, doc_type, img_format,
                                                 self.get_serializer)

            else:
                response = {"message": "Wrong file type", }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get_queryset(self):
        """Return objects for the curent authenticated user only"""
        return self.queryset.filter(user=self.request.user)
