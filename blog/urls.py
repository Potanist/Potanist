from django.conf.urls import patterns, url
from .views import BlogPostListView, BlogPostDetailView

urlpatterns = patterns(
    '',
    url(r'^$', BlogPostListView.as_view(), name='blog_view'),
    url(r'^(?P<pk>[0-9]+)/$', BlogPostDetailView.as_view(), name='blogpost_detailview'),
)
