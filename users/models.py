# Django
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Stripe
from stripeAPI.customer import create_customer

# Commons
from orders.common import OrderStatus


# AbstractUser - (Ver explicación al final)
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)


    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def billing_profile(self):
        return self.billingprofile_set.filter(default=True).first()


    @property
    def description(self):
        return 'Descripción para el usuario {}'.format(self.username)

    def has_customer(self):
        return self.customer_id is not None

    def has_billing_profiles(self):
        return self.billingprofile_set.exists()


    def create_customer_id(self):
        if not self.has_customer():
            customer = create_customer(self)
            self.customer_id = customer.id
            self.save()

    @property
    def billing_profiles(self):
        return self.billingprofile_set.all().order_by('-default')


    def has_shipping_address(self):
        return self.shipping_address is not None

    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')

    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()


    @property
    def addresses(self):
        return self.shippingaddress_set.all()


# Heredamos de User cuándo queramos extender nuevas funcionalidades.
# Con el modelo Proxy no se creará nuevas tablas en la base de datos.
class Customer(User):
    class Meta:
        proxy = True

    def get_products(self):
        return []


# Creamos una relación OneToOneField cuándo queramos añadir nuevos atributos
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField()


'''
# Para crear nuestro propio modelo User...

Cuándo el modelo Proxy o la relación OneToOne no sean suficientes,
procederemos a utilizar 'AbstractUser' o 'AbstractBaseUser'.

La principal diferencia entre 'AbstractUser' o 'AbstractBaseUser'
son los atributos a los cuáles podemos hacer uso.

# Atributos 'AbstractUser'
username
first_name
last_name
email
password
groups
user_permissions
is_staff
is_active
is_superuser
last_login
date_joined

# Atributos 'AbstractBaseUser'
id
password
last_login
'''