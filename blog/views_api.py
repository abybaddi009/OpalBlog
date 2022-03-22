from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets

from rest_framework.response import Response

from .models import Blog, Post
from .serializers import BlogMinSerializer, BlogSerializer, PostMinSerializer, PostSerializer


class CreateUpdateDestroyAuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ('create', 'update', 'destroy'):
            return request.user.is_authenticated
        return True

class BlogListCreateAPIView(viewsets.ViewSet):
    serializer_class = BlogMinSerializer
    full_serializer_class = BlogSerializer
    permission_classes = (CreateUpdateDestroyAuthPermission, )

    def get_queryset(self):
        return Blog.objects.all()

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['pk'])

    def list(self, request):
        serializer = self.full_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        item = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.full_serializer_class(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.created_by != self.request.user:
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.full_serializer_class(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        if item.created_by != self.request.user:
            return Response({'id': "Permissions not present for deletion"}, status=status.HTTP_401_UNAUTHORIZED)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostListCreateAPIView(viewsets.ViewSet):
    serializer_class = PostMinSerializer
    full_serializer_class = PostSerializer
    permission_classes = (CreateUpdateDestroyAuthPermission, )

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(created_by=self.request.user)
        else:
            return Post.objects.filter(published=True)

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs['pk'])

    def list(self, request):
        serializer = self.full_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        item = get_object_or_404(self.get_queryset(), slug=slug)
        serializer = self.full_serializer_class(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.created_by != self.request.user:
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, pk):
        item = self.get_object()
        serializer = self.full_serializer_class(item)
        return Response(serializer.data)

    def destroy(self, request):
        item = self.get_object()
        if item.created_by != self.request.user:
            return Response({'id': "Permissions not present for deletion"}, status=status.HTTP_401_UNAUTHORIZED)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

