
# Django
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('forms.urls', 'forms'), namespace='forms')),
    path('productos/', include(('products.urls', 'products'), namespace='products')),
    path('carrito/', include(('carts.urls', 'carts'), namespace='carts')),
    path('orden/', include(('orders.urls', 'orders'), namespace='orders')),
    path('direcciones/', include(('shipping_addresses.urls', 'shipping_addresses'), namespace='shipping_addresses')),
    path('codigos/', include(('promo_codes.urls', 'promo_codes'), namespace='promo_codes')),
    path('pagos/', include(('billing_profiles.urls', 'billing_profiles'), namespace='billing_profiles')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
