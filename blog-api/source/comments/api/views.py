from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
        )

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.generics import (
        CreateAPIView,
        DestroyAPIView,
        ListAPIView,
        #UpdateAPIView,
        RetrieveAPIView,
        RetrieveUpdateAPIView,
        )

from rest_framework.pagination import (
        LimitOffsetPagination,
        PageNumberPagination,
        )

from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
        IsAdminUser,
        IsAuthenticatedOrReadOnly,
        )

from comments.models import Comment

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from .serializers import (
        CommentDetailSerializer,
        # CommentEditSerializer,
        CommentCreateSerializer,
        CommentListSerializer,
        )


class CommentCreateAPIView(CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(CommentCreateAPIView, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    # subtituido por 'serializer_class'
    # def get_serializer_class(self):
    #     model_type = self.request.GET.get('type')
    #     slug = self.request.GET.get('slug')
    #     parent_id = self.request.GET.get('parent_id', None)
    #     return create_comment_serializer(
    #             model_type=model_type,
    #             slug=slug,
    #             parent_id=parent_id,
    #             user=self.request.user
    #             )

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


#class CommentDeleteAPIView(DestroyAPIView):
#
#    queryset = Comment.objects.all()
#    serializer_class = CommentDetailSerializer
#    # Por padrão, é procurado pela 'pk', implementa a busca pelo 'slug'
#    # Implica na regex em urls.py
#    lookup_field = "slug"
#    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# class CommentEditAPIView(RetrieveAPIView):
# 
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer
#     lookup_field = 'pk'


class CommentDetailAPIView(DestroyModelMixin,UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):

    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name'] # ['title', 'content']

    pagination_class = PostPageNumberPagination

    serializer_class = CommentListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = []
        query = self.request.GET.get('q')
        slug = self.request.GET.get('slug')
        type = self.request.GET.get('type', 'post')
        if slug:
            model_type = type
            model_qs = ContentType.objects.filter(model=model_type)
            if model_qs.exists():
                SomeModel = model_qs.first().model_class()
                obj_qs = SomeModel.objects.filter(slug=slug)
                if obj_qs.exists():
                    content_obj = obj_qs.first()
                    queryset_list = Comment.objects.filter_by_instance(content_obj)
        else:
            queryset_list = Comment.objects.filter(id__gte=0)
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()

        return queryset_list


#class CommentUpdateAPIView(RetrieveUpdateAPIView):
#
#    queryset = Post.objects.all()
#    serializer_class = PostCreateUpdateSerializer
#    # Por padrão, é procurado pela 'pk', implementa a busca pelo 'slug'
#    # Implica na regex em urls.py
#    lookup_field = "slug"
#    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#    def perform_create(self, serializer):
#        serializer.save(user=self.request.user)
