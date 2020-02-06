# Django
from django.db import models

# Models
from users.models import User
from products.models import Product

# Signals
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import m2m_changed

from orders.common import OrderStatus

# Utilities
import uuid
import decimal


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #Uno a muchos
    products = models.ManyToManyField(Product, through='CartProducts') #Relación Muchos a Muchos a través del Modelo CartProducts

    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.05 # 0.5%


    def __str__(self):
        return self.cart_id

    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        if self.order:
            self.order.update_total()


    def update_subtotal(self):
        # List Comprehension
        self.subtotal = sum([
           cp.quantity * cp.product.price for cp in self.products_related()
        ])
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    def products_related(self):
        return self.cartproducts_set.select_related('product')

    @property
    def order(self):
        return self.order_set.filter(status=OrderStatus.CREATED).first()

    def has_products(self):
        return self.products.exists()


class CartProductsManager(models.Manager):

    def create_or_update_quantity(self, cart, product, quantity=1):
        '''
        El siguiente método retornará 2 valores, un objeto y un boleano
        que nos pemitirá saber si el objeto ha sido creado, retorna True
        si ha sido creado, o False en caso contrario.

        El objeto devuelve el objecto, creado o adquirido.
        '''
        object, created = self.get_or_create(cart=cart, product=product)

        if not created:
            '''
            El objeto es de tipo 'CartProducts'
            '''
            quantity = object.quantity + quantity

        object.update_quantity(quantity)
        return object

class CartProducts(models.Model):
    '''
    De esta forma conseguimos que un carrito pueda tener
    Muchos CartProducts, y un Producto, de igual forma,
    también podrá tener muchos CartProducts.
    '''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()



def set_card_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()

pre_save.connect(set_card_id, sender=Cart)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(update_totals, sender=Cart.products.through)