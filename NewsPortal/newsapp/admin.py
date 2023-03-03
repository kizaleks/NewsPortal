from django.contrib import admin
from .models import Post, Category,Author, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):

    list_display = ('author', 'categoryType', 'dateCreation','title','text')
    list_filter = ('author', 'categoryType', 'dateCreation','postCategory')
    search_fields = ('categoryType', 'dateCreation', 'title')


admin.site.register(Author,)
admin.site.register(Category,)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory,)
admin.site.register(Comment,)
