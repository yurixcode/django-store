'''
Para registrar las siguientes funciones es necesario
lo siguiente. Importar template, y crear una nueva
instancia de Library con tal de usarla cómo decorador.
'''

from django import template

register = template.Library()

@register.filter()
def quantity_product_format(quantity=1):
    return '{} {}'.format(quantity, 'productos' if quantity > 1 else 'producto')

@register.filter()
def quantity_add_format(quantity=1):
    return '{} {}'.format(
        quantity_product_format(quantity),
        'agregados' if quantity > 1 else 'agregado'
    )