# Models
from .models import Cart

def get_or_create_cart(request):
    '''
    En el siguiente if estamos indicando, que si
    el usuario está autenticado, se devuelve el usuario,
    con el método 'request.user', en caso contrario se
    devolverá 'None'.
    '''
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id') #None si no existe
    cart = Cart.objects.filter(cart_id=cart_id).first() # [] -> None

    if cart is None:
        cart = Cart.objects.create(user=user)

    if user and cart.user is None:
        cart.user = user
        cart.save()
    
    request.session['cart_id'] = cart.cart_id

    return cart

# Ejemplo, no lo usa nadie, podría ser abstracta
def cartExample(request):
    '''
    Creando, obteniendo y eliminando una sesión
    '''
    # Crear una session
    request.session['cart_id'] = '123' #Dic

    # Obtenemos el valor de una session
    valor = request.session.get('cart_id')
    print(valor)

    # Eliminar session
    valor = request.session['cart_id'] = None
    print(valor)

    return render(request, 'carts/cart.html', {

    })


def destroy_cart(request):
    request.session['cart_id'] = None