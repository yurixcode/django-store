# Django
from django.urls import path

# Views
from . import views

# No es necesario añadir lo siguiente si la las rutas 
# principales tienen un namespace definido para
# cada aplicación. '''
app_name = 'products'

urlpatterns = [
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'), #id -> llave primaria

]