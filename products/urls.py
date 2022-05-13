"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""

from django.urls import path
from . import views
from .views import *

app_name = "products"

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('ordersuccess/', OrderSuccessPageView.as_view(), name ='ordersuccess'),
    path('<int:pk>/', views.product_detail, name='product_details'),
    path('cart/', cart, name='cart'),
    path('accountpage/', AccountPageView.as_view(), name ='accountpage'),
    path('women/', WomenPageView.as_view(), name='women'),
    path('men/', MenPageView.as_view(), name='men'),
    path('decorations/', DecorationsPageView.as_view(), name='decorations'),
    path('accessories/', AccessoriesPageView.as_view(), name='accessories'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_cart'),
    path('remove-one-from-cart/<int:pk>/', remove_one_from_cart, name='remove_cart_one'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove_cart'),
    path('checkout/', checkout, name='checkout')
]