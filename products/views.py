from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower


def all_products(request, category_slug=None):
    """ A view to show all products, including sorting and search queries """

    categories = None
    products = None
    query = None
    sort = None
    direction = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
       
    else:
        products = Product.objects.all().filter(is_available=True)  # Display only available products
       

    # Search and sort products
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query) 
            products = products.filter(queries)
            
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)