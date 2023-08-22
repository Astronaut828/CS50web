from .models import Subscriber, BlogPost
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Create a new sender
        subscriber = Subscriber(name=name, email=email, message=message)
        subscriber.save()
        return redirect('homepage:index')

    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def spotlight(request):
    posts_list = BlogPost.objects.all().order_by('-id')
    paginator = Paginator(posts_list, 3)  # Show 3 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'spotlight.html', {'posts': posts})

def portfolio(request):
    return render(request, "portfolio.html")