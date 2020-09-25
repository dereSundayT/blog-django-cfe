from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from posts.models import Post

# having different serializers is not a must


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'publish', 'content']


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='post-api:detail', lookup_field='slug')

    class Meta:
        model = Post
        fields = ['title', 'user', 'slug', 'content', 'url']