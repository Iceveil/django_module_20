from django.views.generic import ListView, DetailView

from .models import Article


class BasedView(ListView):
    template_name = 'blogapp/article_list.html'
    model = Article
    context_object_name = 'articles'
    queryset = (
        Article.objects.select_related('author').
                select_related('category').
                prefetch_related('tags').
                defer('content')
                )