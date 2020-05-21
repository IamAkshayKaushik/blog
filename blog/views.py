from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.models import User
from django.views import View


class Home(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Post.objects.select_related('author__user_profile')
        search = self.request.GET.get('search', '')
        if len(search) > 0:
            queryset = queryset.filter(Q(title__icontains=search)
                                       | Q(description__icontains=search))
            messages.success(self.request, f'You search for {search}.', extra_tags='alert')
        return queryset


class PostDetailView(generic.DetailView):
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
    queryset = Post.objects.select_related('author__user_profile')
    model = Post
    template_name = 'blog/single-post-1.html'




