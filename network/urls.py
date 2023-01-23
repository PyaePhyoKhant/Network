
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("post/add/", login_required(views.PostCreateView.as_view()), name='post-add'),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
