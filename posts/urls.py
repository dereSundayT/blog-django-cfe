from django.urls import path
from .views import post_create,post_delete,post_detail,post_list,post_update

app_name = 'posts'
urlpatterns = [
    path('create/',post_create,name='create'),
    path('<str:slug>/',post_detail,name='detail'),
    path('',post_list,name='list'),
    path('<str:slug>/update/',post_update,name='update'),
    path('<str:slug>/delete/',post_delete,name='delete'),
]
