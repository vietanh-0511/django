from django.urls import path
from .views import category, add_to_cart, cart_view, checkout_form, checkout_process, index, login_process, login_view, logout, register_process, register_view, remove, search_view, update_qty
urlpatterns = [
    path('', index, name='index'),
    path('category/<int:id>', category, name='category'),
    path('search', search_view, name='search'),
    path('register', register_view, name="register_view"),
    path('register_process', register_process, name="register_process"),
    path('login', login_view, name="login_view"),
    path('login_process', login_process, name="login_process"),
    path('logout', logout, name="logout"),
    path('add_to_cart/<int:id>/', add_to_cart, name="add_to_cart"),
    path('cart', cart_view, name="cart"),
    path('update_qty/<int:id>/', update_qty, name="update_qty"),
    path('remove/<int:id>/', remove, name="remove"),
    # path('inc_qty/<int:id>/', inc_qty, name="inc_qty"),
    # path('dec_qty/<int:id>/', dec_qty, name="dec_qty"),
    path('checkout', checkout_form, name="checkout"),
    path('checkout_process', checkout_process, name="checkout_process"),
]
