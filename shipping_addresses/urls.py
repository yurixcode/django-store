# Django
from django.urls import path

# Views
from . import views

app_name = 'shipping_addresses'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_addresses'),
    path('nueva', views.create, name='create'),
    path('editar/<int:pk>', views.ShippingAddressUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>', views.ShippingAddressDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
]