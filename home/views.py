from django.shortcuts import render

# Create your views here.
def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')

def info_page(request):
    """ Info page with sign-up form, Facebook link, and FAQs """
    return render(request, 'home/info.html')


