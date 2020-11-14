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

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # def perform_create(self, serializer):

    #     serializer.save(user=self.request.user)
   
    def create(self, request):
        doc = request.data
        serializer =  serializers.DocumentSerializer(data=doc)
        if serializer.is_valid():     
            obj = serializer.save(user=self.request.user) 
            return img_parse_main.get_sights(obj)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # response = {"status_code": status.HTTP_200_OK,
        #             "message": "Successfully created",
        #             }

        # return Response(response)

    def get_queryset(self):
        """Return objects for the curent authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    # @action(methods=['POST'],detail=False,url_path='upload')
    # def upload_doc(self,request,pk=None):
    #     """Upload doc"""
    #     doc = self.get_object()
    #     serializer = self.get_serializer(
    #         doc,
    #         data=request.data
    #     )
    #     print(request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data.sigh_number,
    #             status=status.HTTP_200_OK
    #         )

    #         return Response(
    #             serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )