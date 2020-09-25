from django.urls import path
from .views import PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostUpdateAPIView


urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<str:slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<str:slug>/edit', PostUpdateAPIView.as_view(), name='update'),
    path('<str:slug>/delete', PostDeleteAPIView.as_view(), name='delete'),
]
