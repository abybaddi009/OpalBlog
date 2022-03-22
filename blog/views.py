from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from rest_framework import status

from .models import Blog, Post


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=status.HTTP_401_UNAUTHORIZED)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)

class BlogDetailView(generic.ListView):
    slug_url_kwarg = "slug_value"
    slug_field = "slug"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(blog__slug=self.kwargs['slug_value'])
        else:
            posts = Post.objects.filter(blog__slug=self.kwargs['slug_value'], published=True)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.filter(slug=self.kwargs['slug_value']).first()
        return context

class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ['title', 'description']

    def form_valid(self, form):
        blog = form.save(commit=False)
        form.instance.created_by = self.request.user
        blog.save()
        return super(BlogCreateView, self).form_valid(form)

class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ['title', 'description']
    slug_url_kwarg = "slug_value"
    slug_field = "slug"

class BlogListView(generic.ListView):

    def get_queryset(self):
        return Blog.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostCreateView(generic.CreateView):
    model = Post
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.filter(slug=self.kwargs['slug_value']).first()
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        else:
            return super(PostCreateView, self).form_invalid(form)
        
        # fetch the current blog and update
        blog = Blog.objects.filter(slug=self.kwargs['slug_value']).first()
        post = form.save(commit=False)
        post.blog = blog
        post.save()
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(JsonableResponseMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content']
    slug_url_kwarg = "slug_value"
    slug_field = "slug"
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        if not (self.request.user.is_authenticated and self.request.user == self.get_object().created_by):
            form.errors['message'] = "User not authorized"
            form.errors['status'] = status.HTTP_401_UNAUTHORIZED
            return super(PostUpdateView, self).form_invalid(form)
        
        # fetch the current post and update
        return super(PostUpdateView, self).form_valid(form)

class PostDetailView(generic.DetailView):
    slug_url_kwarg = "slug_value"
    slug_field = "slug"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(slug=self.kwargs['slug_value'])
        else:
            posts = Post.objects.filter(slug=self.kwargs['slug_value'], published=True)
        return posts


