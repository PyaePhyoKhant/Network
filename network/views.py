from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Post


class PostCreateView(CreateView):
    model = Post
    fields = ['description']
    

class PostUpdateView(UpdateView):
    model = Post
    fields = ['description']
    
    
@csrf_exempt
@login_required
def update_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.get(pk=int(data['id']))
    if post.created_by != request.user:
        return JsonResponse({"error": "Access rights error."}, status=403)
    post.description = data['description']
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=200)
    

class PostListView(ListView):
    model = Post
    queryset = Post.objects.order_by('-created_at')
    template_name = 'network/index.html'
    paginate_by = 10
    
    
class PostFollowingView(ListView):
    model = Post
    template_name = 'network/following.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(created_by__in=self.request.user.following.all()).order_by('-created_at')
    
    
class UserDetailView(DetailView):
    model = User
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_in_following'] = self.request.user.is_in_following(context['object'])
        # to avoid conflict with template `user`
        del context['user']
        return context


def change_following(request):
    other_user = User.objects.get(id=int(request.POST['user_id']))
    if request.user.is_in_following(other_user):
        request.user.following.remove(other_user)
    else:
        request.user.following.add(other_user)
    return HttpResponseRedirect(reverse('user-detail', kwargs={'pk': other_user.id}))

def index(request):
    return render(request, "network/index.html")


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
