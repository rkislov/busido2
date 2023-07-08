from rest_framework import viewsets, filters
from .serializers import PostSerializer, TagSerializer, ContactSerializer
from .models import Post
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import generics
from taggit.models import Tag
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import send_mail_task


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lower()
        tag = Tag.objects.get(slug=tag_slug)
        return Post.objects.filter(tags=tag)


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['@title', '@content']
    filter_backends = (filters. SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


class FeedBackView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = ContactSerializer(data=request.data)
        if serializer_class.is_valid():
            data = serializer_class.validated_data
            name = data.get('name')
            from_email = data.get('email')
            subject = data.get('subject')
            message = data.get('message')
            send_mail_task(subject, message, from_email, 'roman@kislovs.ru')
            send_mail_task("Спасибо за обращени к нам", "Мы учтем ваши пожелания", 'roman@kislovs.ru', from_email)
            return Response({"success": "Отправлено"})


