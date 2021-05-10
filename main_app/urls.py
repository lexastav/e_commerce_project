from django.urls import path

from .views import test_vew


urlpatterns = [
    path('', test_vew, name='base')
]