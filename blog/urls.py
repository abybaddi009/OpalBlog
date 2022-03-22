from posixpath import basename
from django.urls import path
from rest_framework import routers

from . import views
from . import views_api

app_name = "blog"

urlpatterns = [
    path("", views.BlogListView.as_view(), name="blogs"),
    path("blog/new/", views.BlogCreateView.as_view(), name="blog-create"),
    path("blog/<slug:slug_value>/", views.BlogDetailView.as_view(), name="blog-detail"),
    path("blog/<slug:slug_value>/edit/", views.BlogUpdateView.as_view(), name="blog-update"),
    path(
        "blog/<slug:slug_value>/new/",
        views.PostCreateView.as_view(),
        name="post-create",
    ),
    path("post/<slug:slug_value>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<slug:slug_value>/edit/", views.PostUpdateView.as_view(), name="post-update"),
]

router = routers.SimpleRouter()
router.register(r"blog/api/blogs", views_api.BlogListCreateAPIView, basename="blogs")
router.register(r"blog/api/posts", views_api.PostListCreateAPIView, basename="posts")

urlpatterns += router.urls
