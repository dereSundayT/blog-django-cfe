from django.db.models import Q
from rest_framework.filters import (
    SearchFilter, OrderingFilter
)
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView
from posts.models import Post
from .serializers import PostDetailSerializer, PostListSerializer, PostCreateUpdateSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # u can modify the content u want to save
        # u call a func to create a slug and save or call a saving function to handle that
        serializer.save(user=self.request.user, title='hello')


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = "slug"


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    # obj_data.data['content]
    # ?search=mmmm&ordering=title
    # ?search=mmmm&ordering=-title
    # ?limit=2
    # limit=2&offset=1
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "content", "user__first_name"]
    pagination_class = PostLimitOffsetPagination  # PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        return queryset_list
