from django.urls import path

from .views import test_vew, ProductDetailView


urlpatterns = [
    path('', test_vew, name='base'),
    path('products/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
]