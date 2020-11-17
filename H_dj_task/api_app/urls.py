from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_app import views
from api_app.views import DocumentsViewSet
# create new router object
router = DefaultRouter()
router.register('upload', views.DocumentsViewSet)
app_name = 'api_app'

urlpatterns = [
    path('', include(router.urls)),

]
