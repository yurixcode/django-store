# Django
from django import template

#Al crear la siguiente instancia, ya podremos declarar nuestros filters
register = template.Library()

@register.filter()
def price_format(value):
    '''
    Esto se usa en el template.

    Ejemplo: 
    ${{ product.price | price_format }}

    P.D. Hay que importarlo. Ver ejemplo en 'template/add.html'
    '''
    return '${0:.2f}'.format(value)  #Decimal con 2 digítos