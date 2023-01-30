
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("change_following", views.change_following, name="change_following"),
    path("post/add/", login_required(views.PostCreateView.as_view()), name='post-add'),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name='user-detail'),
    path("", views.PostListView.as_view(), name='index'),
    # path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
