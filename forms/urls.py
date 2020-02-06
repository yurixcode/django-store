from django.urls import path
from .views import index, login_view, logout_view, register
from products.views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('registro/', register, name='register'),
]