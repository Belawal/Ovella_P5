from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Rigyq2SCQqrl5JdM1PKK0mfT4BEy6FN7kgkFPwqZTFPvnjhmQ6y1CTsHH7lg4w6nPJ5WnLXgoCe0RF7DeOdrdpf00GyfNJdx4',
        'client_secret': 'test client secret',

    }

    return render(request, template, context)
    