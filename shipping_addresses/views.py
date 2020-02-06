# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect

# Django Utilities
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

# Django Views
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Models
from .models import ShippingAddress

# Forms
from .forms import ShippingAddressForm

# Utils
from carts.utils import get_or_create_cart
from orders.utils import get_or_create_order


class ShippingAddressListView(LoginRequiredMixin, ListView):
    login_url = 'forms:login'

    model = ShippingAddress
    template_name = 'shipping_addresses/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'forms:login'
    success_message = 'Dirección actualizada exitosamente'

    model = ShippingAddress
    form_class = ShippingAddressForm
    template_name = 'shipping_addresses/update.html'

    def get_success_url(self):
        return reverse('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAddressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'forms:login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'
    success_url = reverse_lazy('shipping_addresses:shipping_addresses')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_addresses:shipping_addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        if self.get_object().has_orders():
            return redirect('shipping_addresses:shipping_addresses')

        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='forms:login')
def create(request):
    form = ShippingAddressForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()

        shipping_address.save()
        
        if request.GET.get('next'):
            if request.GET['next'] == reverse('orders:address'):
                '''
                Si el usuario añade una nueva dirección desde
                el proceso de pago, haremos lo siguiente ->
                '''
                cart = get_or_create_cart(request)
                order = get_or_create_order(cart, request)

                order.update_shipping_address(shipping_address)

                return HttpResponseRedirect(request.GET['next'])

        messages.success(request, 'Dirección creada exitosamente')
        return redirect('shipping_addresses:shipping_addresses')

    return render(request, 'shipping_addresses/create.html', {
        'form': form
    })

@login_required(login_url='forms:login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')
    
    if request.user.has_shipping_address():
        #Obtener la antigua dirección principal y cambia el estado a False
        request.user.shipping_address.update_default(default=False)

    shipping_address.update_default(default=True)

    return redirect('shipping_addresses:shipping_addresses')
