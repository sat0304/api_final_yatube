from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


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
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if following == user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        elif Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                'Подписка уже создана ранее!'
            )
        else:
            return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following', )
            )
        ]
