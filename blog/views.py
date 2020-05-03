from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Post
from django.contrib.auth.models import User
from django.views import View

posts = [{
    'title': "this is post title",
    'body': 'this is post body'
},
    {
        'title': "this is post title",
        'body': 'this is post body'
    },
    {
        'title': "this is post title",
        'body': 'this is post body'
    }
]


class Home(generic.ListView):
    model = Post
    template_name = 'blog/home.html'

    # def get(self, request):
    #     return render(request, 'base.html', {'posts': posts})

    def get_queryset(self):
        queryset = Post.objects.prefetch_related('author__user_profile').all()
        return queryset


class PostDetailView(generic.DetailView):
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
    queryset = Post.objects.prefetch_related('author__user_profile').all()
    model = Post
    template_name = 'blog/single-post-1.html'




