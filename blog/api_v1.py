from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .serializers import PostSerializer
from .models import Post
from django.conf.urls import url
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


# 함수형
def post_list(request):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    json_utf8_strging = JSONRenderer().render(serializer.data)
    return HttpResponse(json_utf8_strging,
                        content_type='application/json; charset=utf8')


class PostPagination(PageNumberPagination):
    page_size = 10


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

urlpatterns = [
    url(r'^post/list/$', post_list, name='api_v1_post_list'),
    url(r'^post/list_json/$', PostListAPIView.as_view(), name='api_v1_post_list_json')
]