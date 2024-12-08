from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from cart.forms import CartAddProductForm
from django.contrib.postgres.search import SearchRank,SearchVector,SearchQuery
# Create your views here.

def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category)

    return render(request,'shop/product/list.html',
                            {'category': category,
                            'categories': categories,
                            'products': products,
                            'total_product_count': len(products),
                            'cart_product_form': cart_product_form})

def product_detail(request, id, slug):
 product = get_object_or_404(Product,
 id=id,
 slug=slug)
 return render(request,
 'shop/product/detail.html',
 {'product': product})


def home(request):
   try:
        products = Product.objects.all()[5]
   except IndexError:
        products = Product.objects.all()

   return render(request,'shop/home.html',{'products':products})

def verify(request):
    return render(request,'shop/googleb0dbb8bde61b8b0b.html')

def contact_page(request):
    return render(request,'shop/contactus.html')

def policies_page(request):
    return render(request,'shop/policies.html')


def post_search(request):
    query = None
    results = []
    
    if 'search' in request.GET:
        query = request.GET.get('search')
        print(query)
        search_vector = SearchVector('name')
        search_query = SearchQuery(query)

        results = Product.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')
        print(results)
    return render(request, 'shop/search.html', {
        'query': query,
        'results': results,
    })

