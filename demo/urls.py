from django.contrib.auth import views as auth_views
from django.urls import path

from demo import views
from demo.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),


    path('about/', about, name='about'),
    path('', catalog, name='catalog'),
    path('contact/', contact, name='contact'),
    path('cart/', cart, name='cart'),
    path('orders/', orders, name='orders'),
    path('product/<pk>', product, name='product'),

]
