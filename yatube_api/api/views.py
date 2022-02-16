from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer
from posts.models import Comment, Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """Набор правил для обработки текстовых постов авторов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    """Набор правил для обработки комментариев к постам авторов."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор правил для обработки групп постов авторов."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Набор правил для обработки подписок на авторов."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('following__username', 'user__username')

    def perform_create(self, serializer):
        following = serializer.validated_data['following']
        if Follow.objects.filter(
                user=self.request.user,
                following=following
            ).exists():
            raise ValidationError('Подписка уже создана!')
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset_1 = Follow.objects.filter(user=self.request.user)
        return queryset_1
