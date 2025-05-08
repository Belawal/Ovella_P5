# Importing necessary functions and modules from Djangofrom django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

# Importing models that we will use in this file
from .models import Product, Category

# ----------------------------
# Show all products page
# This page shows all items in the shop
# It also lets user search or filter by category
# ----------------------------
def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:# If user searched or clicked a filter
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET: # If user searched something
            query = request.GET['q']
            if not query: # If user didn't type anything
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            # Search in name or description of products
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Send this info to the webpage
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products.html', context)

# ----------------------------
# Show one product page
# This page opens when user clicks a product
# ----------------------------
def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id) # Get the product or show 404 error

    # Send this info to the webpage
    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)