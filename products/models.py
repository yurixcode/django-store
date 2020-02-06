# Django
from django.db import models
from django.utils.text import slugify

# Signals
from django.db.models.signals import pre_save

# Uttils
import uuid


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    image = models.ImageField(upload_to='products/', null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0) #12234.50

    slug = models.SlugField(null=False, blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)


    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title) # 'slugify' genera un slug automático. GRACIAS DJANGO
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

def set_slug(sender, instance, *args, **kwargs): #callback
    print('Estoy dentro de la función')
    if instance.title and not instance.slug:
        print('Estoy dentro del if')
        slug = slugify(instance.title)

        while Product.objects.filter(slug=slug).exists():
            print('Estoy dentro del while!')
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )

        instance.slug = slug


    print(sender); print(instance)

pre_save.connect(set_slug, sender=Product)