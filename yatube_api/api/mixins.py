from rest_framework import mixins, viewsets


class FollowListOrCreate(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass
