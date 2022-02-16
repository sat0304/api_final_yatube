from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Компоновщик-анализатор текстовых постов авторов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Компоновщик-анализатор комментариев к текстовым постам авторов."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('author', 'post', 'text', 'created', 'id')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    """Компоновщик-анализатор групп постов авторов."""

    class Meta:
        fields = ('title', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Компоновщик-анализатор подписок на авторов."""
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    def validate(self, data):
        request = self.context.get('request')
        following = self.context['request'].user
        if request.user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return (data, Response(status=status.HTTP_201_CREATED))

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following', )
            )
        ]
