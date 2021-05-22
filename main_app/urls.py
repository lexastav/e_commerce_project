from django.urls import path

from .views import(
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<str:ct_model>/<str:slug>', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change_quantity/<str:ct_model>/<str:slug>', ChangeQuantityView.as_view(), name='change_quantity'),
]