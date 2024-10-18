from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path("base/", Baseview, name="base"),
    path("home/", Homeview, name="home"),
    path("products/", Productview, name="products"),
    path('search/', views.Search, name='search'),
    path('products/<int:id>/', views.Product_Detail_Page, name='product_detail'),
    path('contact/', views.Contact_Page, name='contact'),
    path('about/', about, name='about'),

    path("register/", views.HandleRegister,name="register"),
    path("login/", views.HandleLogin,name="login"),
    path("logout/", views.HandleLogout,name="logout"),


    #Cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart/wishlist/', views.wishlist, name='wishlist'),
    path('cart/checkout/', views.Check_out, name='checkout'),
    path('payment/', PaymentView.as_view(), name='payment'),

    path('Cart/placeorder/', views.Place_Order, name='place_order'),

    path('success/',views.Success, name="success")
]

# settings.py
