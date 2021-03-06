from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import(
    BaseView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView,
    CheckoutView,
    MakeOrderView,
    LoginView,
    RegistrationView,
    ProfileView,
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change_quantity/<str:slug>/', ChangeQuantityView.as_view(), name='change_quantity'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make_order/', MakeOrderView.as_view(), name='make_order'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
]