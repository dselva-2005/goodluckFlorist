from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Category,SiteReviewModel,CoreCategory
from cart.forms import CartAddProductForm, MessageForm
from django.contrib.postgres.search import SearchRank,SearchVector,SearchQuery
from .forms import ReviewForm,SiteReviewForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .tasks import sendmessage

# Create your views here.

def product_list(request,category_slug=None):
    page_number = request.GET.get('page', 1)
    category = None
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.filter(available=True)
    
    total_product_count = Product.objects.all().count()
    paginator = Paginator(products,4)
    categories = Category.objects.all()
    core_categories = CoreCategory.objects.all()
    cart_product_form = CartAddProductForm()
    products = paginator.get_page(page_number)

    return render(request,'shop/product/list.html',
                            {'category': category,
                            'categories': categories,
                            'core_categories': core_categories,
                            'products': products,
                            'total_product_count': total_product_count,
                            'page_product_count': len(products),
                            'cart_product_form': cart_product_form})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug)
    form = ReviewForm({"product":product,
                       "rating":(5,'Excellent'),})
    return render(request,
    'shop/product/detail.html',
    {'product': product,
    'form':form})


def home(request):
   try:
        products = Product.objects.all()[:6]
   except IndexError:
        products = Product.objects.all()

   return render(request,'shop/home.html',{'products':products})

def verify(request):
    return render(request,'shop/googleb0dbb8bde61b8b0b.html')

def contact_page(request):
    message_form = MessageForm()
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            # Extract data from form
            cd = message_form.cleaned_data
            email = cd['email']
            subject = f"Message from {cd['name']} at Goodluck Florist"
            message_body = f"Name: {cd['name']}\nEmail: {cd['email']}\n\nMessage:\n{cd['message']}"
            
            sendmessage.delay(subject,message_body,email)
            
            messages.success(request, "Your message has been sent successfully!")
        else:
            messages.error(request, "There was an error with your form. Please correct it and try again.")

    return render(request, 'shop/contactus.html', {"form": message_form})

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

@require_POST
def review_form(request):
    form = ReviewForm(request.POST)
    referring_url = request.META.get('HTTP_REFERER', '/')
    if form.is_valid():
        form.save()
        messages.success(request,"review submitted")
    else:
        messages.error(request,'review not valid')
    return redirect(referring_url)

def feedback(request):

    reviews_count = SiteReviewModel.objects.all().count()
    if reviews_count>5:
        reviews = SiteReviewModel.objects.all()[:5]
    else:
        reviews = SiteReviewModel.objects.all()
    if request.method == "POST":
        form = SiteReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Feedback submitted')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        else:
            messages.error(request,'Failed to submit the Feedback')
            return render(request,'shop/feedback.html',{'form':form,
                                                'reviews':reviews})
    form = SiteReviewForm()
    return render(request,'shop/feedback.html',{'form':form,
                                                'reviews':reviews})