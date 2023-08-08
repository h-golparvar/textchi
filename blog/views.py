from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views import View
from . import models
from .forms import CommentForm


class BlogRootView(View):
    def get(self, request):
        return render(request, 'blog/root.html')


class BlogPostView(View):
    def get(self, request, slug):
        post = get_object_or_404(models.Post, slug=slug)
        category = models.Category.objects.all()
        tags = models.Tag.objects.all()

        return render(request, 'blog/blogpost.html', {'post': post, 'categories': category, 'tags': tags})


class AddCommentView(View):
    def post(self, request):
        form = CommentForm(request.POST)
        
