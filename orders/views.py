# Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from django.db.models.query import EmptyQuerySet
from django.db import transaction

# Threads
import threading

# Utils
from .utils import get_or_create_order
from .utils import breadcrumb
from .utils import destroy_order

from carts.utils import destroy_cart
from carts.utils import get_or_create_cart

# Decorators
from .decorators import validate_cart_and_order

# Models
from .models import Order
from shipping_addresses.models import ShippingAddress
from charges.models import Charge

# Mails
from .mails import Mail


class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'forms:login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        # return EmptyQuerySet # []
        return self.request.user.orders_completed()


@login_required(login_url='forms:login')
@validate_cart_and_order
def order(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    if not cart.has_products():
        return redirect('carts:cart')

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })


@login_required(login_url='forms:login')
@validate_cart_and_order
def address(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)
    if not cart.has_products():
        return redirect('carts:cart')

    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses()

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'can_choose_address': can_choose_address,
        'breadcrumb': breadcrumb(address=True),
    })


@login_required(login_url='forms:login')
def select_address(request):
    shipping_addresses = request.user.addresses

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })


@login_required(login_url='forms:login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)
    
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    
    order.update_shipping_address(shipping_address)

    return redirect('orders:address')


@login_required(login_url='forms:login')
@validate_cart_and_order
def payment(request, cart, order):
    if not cart.has_products() or order.shipping_address is None:
        return redirect('carts:cart')
    
    billing_profile = order.get_or_set_billing_profile()

    return render(request, 'orders/payment.html', {
        'cart':cart,
        'order':order,
        'billing_profile': billing_profile,
        'breadcrumb': breadcrumb(address=True, payment=True)
    })


@login_required(login_url='forms:login')
@validate_cart_and_order
def confirm(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)
    if not cart.has_products() or order.shipping_address is None or order.billing_profile is None:
        return redirect('carts:cart')

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'breadcrumb': breadcrumb(address=True, confirmation=True, payment=True)
    })

@login_required(login_url='forms:login')
@validate_cart_and_order
def cancel(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    
    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Pedido cancelado')
    return redirect('forms:index')

@login_required(login_url='forms:login')
@validate_cart_and_order
def complete(request, cart, order):
    # cart = get_or_create_cart(request)
    # order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    charge = Charge.objects.create_charge(order)
    if charge:
        with transaction.atomic():
            '''Ejecutando un with con atomic(), ejecutará como una transacción,
            o se ejecuta todo, o no se ejecutará nada...'''
            order.complete()

            # Envíar correo de forma asíncrona
            thread = threading.Thread(target=Mail.send_complete_order, args=(
                order, request.user
            ))
            thread.start()

            # Mail.send_complete_order(order, request.user)

            destroy_cart(request)
            destroy_order(request)

            messages.success(request, 'Compra completada exitosamente')

    return redirect('forms:index')


