from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogRootView.as_view(), name='root'),
    path('<slug:slug>/', views.BlogPostView.as_view(), name='blog-post'),
    path('comment/', views.AddCommentView.as_view(), name='add-comment'),
]
