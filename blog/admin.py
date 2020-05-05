from django.contrib import admin
from .models import Post, Category, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'author')

    def get_category(self, obj):
        return ",".join([p.name for p in obj.category.all()])


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Profile)
