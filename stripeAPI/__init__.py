import stripe
# from django.conf import settings
from decouple import config


stripe.api_key = config('STRIPE_PRIVATE_KEY') #Env

