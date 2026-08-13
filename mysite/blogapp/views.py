from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


# Create your views here.


class ArticleListView(ListView):
    queryset = (
        Article.objects
        .select_related("author", "category")
        .prefetch_related("tags")
        .defer("content")
    )
