from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import CommentSerializer, FollowSerializer
from .serializers import GroupSerializer, PostSerializer
from posts.models import Comment, Follow, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    """Набор правил для обработки текстовых постов авторов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated, )

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
    permission_classes = (IsAuthenticated, )


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """Набор правил для обработки подписок на авторов."""
    pass

