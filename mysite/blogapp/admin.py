from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Article, Author, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_date', 'author', 'category', )
    list_display_links = ('title', 'content', 'pub_date', 'author', 'category', )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    list_display_links = ('name', 'bio')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)