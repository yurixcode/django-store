# Django
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

# Models
from .models import Product


class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        # context['products'] = context['object_list']
        # print(context)

        return context

class ProductDetailView(DetailView): #id -> pk
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs):
        ''' No aplicamos ningún cambio, sin embargo
        de este modo seremos capaces de imprimir el
        contexto, y así poder conocer su contenido :) '''
        
        context = super().get_context_data(**kwargs)

        # print(context) 
        return context

class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def query(self):
        '''
        Obtenemos el query ingresado en el formulario.
        '''
        return self.request.GET.get('q')

    def get_queryset(self):
        '''
        Hacemos una búsqueda dinámica, a través del query buscado
        en el formulario, par eso sustituimos el método get_queryset
        '''
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()

        return context