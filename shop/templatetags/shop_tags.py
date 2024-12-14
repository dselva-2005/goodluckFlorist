from django import template
from shop.models import Product
register = template.Library()

@register.simple_tag
def getSingleImg(product_id):
    product = Product.objects.get(id=product_id)
    return product.images.first().image.url

@register.filter
def rangeOf(value):
    return range(value)