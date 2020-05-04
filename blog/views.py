from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.models import User
from django.views import View


class Home(generic.ListView):
    queryset = Post.objects.select_related('author__user_profile').all()
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 2


class PostDetailView(generic.DetailView):
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
    queryset = Post.objects.select_related('author__user_profile').all()
    model = Post
    template_name = 'blog/single-post-1.html'




