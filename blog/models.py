import random
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pic')
    description = models.TextField(default='Default description', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 and img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        db_table = 'Profile'


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='1', related_name='author_category')

    # def save(self, *args, **kwargs):
    #     self.url = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"

    class Meta:
        db_table = 'Category'


class Post(models.Model):
    STATUS_CHOICES = (
                        ('draft', 'Draft'),
                        ('published', 'Published'),
                    )
    title = models.CharField(max_length=75, null=False, blank=False)
    description = models.TextField()
    feature_image = models.ImageField(upload_to='post/feature_image', default='default.jpg')
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='1', related_name='author_posts')
    category = models.ManyToManyField(Category, related_name='category_posts')
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

    def get_random_posts_by_category(self):
        return Post.objects.select_related('author__user_profile').filter(category__in=self.category.all()).order_by('?')[:3]
        # random_post = Post.objects.filter(category__in=self.category.all()).values_list('id',flat=True)
        # print(random_post)
        # random_ids = random.sample(list(random_post), 3)
        # print(random_ids)
        # return Post.objects.filter(id__in=random_ids)

    class Meta:
        db_table = 'Post'
        ordering = ('-publish',)
