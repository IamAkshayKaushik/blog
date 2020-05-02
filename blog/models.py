from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='1', related_name='author_category')

    def save(self, *args, **kwargs):
        self.url = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Category'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=75, null=False, blank=False)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='1', related_name='author_posts')
    category = models.ManyToManyField(Category)
    slug = models.SlugField(max_length=100, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.IntegerField(default=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('blog:post_detail', kwargs={"slug": self.slug})
        return f"/{self.slug}/"

    class Meta:
        db_table = 'Post'
        ordering = ('-publish',)
