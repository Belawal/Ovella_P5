from django.shortcuts import render, redirect, reverse, HttpResponse
# Create your views here.

def view_bag(request):
    """ Show what's in the bag (cart page) """
    # Just show the bag.html page so people can see their stuff
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Put stuff in the bag (like when you add to cart) """

    # Get the number we picked (like 2 apples)
    quantity = int(request.POST.get('quantity'))

    # Where we came from, so we can go back there after adding
    redirect_url = request.POST.get('redirect_url')

    # Get the bag from the session, or start with an empty one
    bag = request.session.get('bag', {})

    # If it's already in the bag, just add more to the number
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        # If it's not in the bag, add it with the number
        bag[item_id] = quantity

    # Save the updated bag so it remembers
    request.session['bag'] = bag

    # Print it out in the console just to check (for testing)
    print(request.session['bag'])

    # Go back to the page we were on
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Change how many of the thing we want in the bag"""
    # Get the number we typed in the box (comes as text, so turn it into a number)
    quantity = int(request.POST.get('quantity'))
    # Get our bag from the session (like a saved cart), or make an empty one if it doesn't exist
    bag = request.session.get('bag', {})
    # If we want more than 0, we update the number
    if quantity > 0:
        bag[item_id] = quantity  # Just put the new number in the bag
    else:
        bag.pop(item_id)  # If we typed 0 or less, take it out of the bag
    # Save the new bag so it remembers
    request.session['bag'] = bag
    # Go back to look at the bag page
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Take something out of the bag (like a delete)"""

    try:
        # Get the bag like before
        bag = request.session.get('bag', {})
        # Remove the thing we don’t want anymore
        bag.pop(item_id)
        # Save the bag again so it updates
        request.session['bag'] = bag
        # Say “OK, it worked”
        return HttpResponse(status=200)
    
    except Exception as e:
        # Something broke just say it didn’t work
        return HttpResponse(status=500)

