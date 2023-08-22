from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator

from .models import User, Post, Following

def index(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 10)  # Show x posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "is_index_page": True,
    }

    return render(request, 'network/index.html', context)


@login_required(login_url='login')
def following(request):
    # Get all users that the current user is following
    following_users = Following.objects.filter(user=request.user).values_list('following_user', flat=True)

    # Get all posts from those users
    post_list = Post.objects.filter(Q(user__in=following_users)).order_by('-timestamp')
    paginator = Paginator(post_list, 10)   # Show x posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/following.html", {
        "page_obj": page_obj,
    })


@login_required(login_url='login')
def user(request):
    # Fetch the current user's information
    user = get_object_or_404(User, id=user_id)
    user_info = Following.objects.filter(user=request.user)
    user_posts = Post.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, "network/user.html", {
        "user": user,
        "user_posts": user_posts,
        "user_info": user_info,
        "is_user_page": True,
    })


@login_required(login_url='login')
def user_page(request, user_id):
    # Fetch the profile user's information
    profile_user = get_object_or_404(User, id=user_id)

    # Check if the current user is following the profile user
    following_status = Following.objects.filter(user=request.user, following_user=profile_user).exists()

    # Retrieve the counts
    following_count = Following.objects.filter(user=profile_user).count()
    followers_count = Following.objects.filter(following_user=profile_user).count()

    #get user Posts
    post_list = Post.objects.filter(user=profile_user).order_by('-timestamp')
    paginator = Paginator(post_list, 10)  # Show x posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile_user': profile_user,
        "page_obj": page_obj,
        'following_status': following_status,
        'following_count': following_count,
        'followers_count': followers_count,
        'is_user_page': True
    }
    return render(request, 'network/user.html', context)


@login_required
def follow_toggle_view(request):
    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        user = request.user

        # Toggle the following status
        following_status = toggle_follow_status(user, profile_id)

        # Retrieve the updated counts
        following_count = Following.objects.filter(user=profile_user).count()
        followers_count = Following.objects.filter(following_user=profile_user).count()

        return JsonResponse({
            "following_status": following_status,
            "following_count": following_count,
            "followers_count": followers_count
        })

    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required
def create_post(request):
    if request.method == "POST":
        # Retrieve the post body text from the request
        body_text = request.POST.get("body_text", "")
        user = request.user
        timestamp = timezone.now()

        # Create a new post object and save it to the database
        post = Post(user=user, body_text=body_text, timestamp=timestamp)
        post.save()

        return JsonResponse({"message": "Post created successfully."})
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


@method_decorator(login_required, name='dispatch')
class UpdatePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.body_text = request.POST.get('text')
        post.save()
        return JsonResponse({"body_text": post.body_text})


def profile_view(request, profile_user_id):
    # Get the profile user based on the profile_user_id
    profile_user = User.objects.get(id=profile_user_id)

    # Determine the following status of the current user and profile user
    following_status = Following.objects.filter(user=request.user, following_user=profile_user).exists()

    context = {
        'profile_user': profile_user,
        'following_status': following_status
    }

    return render(request, 'user.html', context)


def follow_toggle_view(request):
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        user = request.user

        # Check if the user is already following the profile
        try:
            following_obj = Following.objects.get(user=user, following_user_id=profile_id)
            following_obj.delete()  # If following exists, delete it (unfollow)
            following_status = False
        except Following.DoesNotExist:
            Following.objects.create(user=user, following_user_id=profile_id)  # If not following, create it (follow)
            following_status = True

        return JsonResponse({'following_status': following_status})

    return JsonResponse({'error': 'Invalid request method'})


@login_required
@require_POST
def like_toggle_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.liked_by.all():
            post.likes -= 1
            post.liked_by.remove(user)
        else:
            post.likes += 1
            post.liked_by.add(user)

        post.save()
        return JsonResponse({"likes": post.likes})
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post does not exist"}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
