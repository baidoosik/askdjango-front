from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .serializers import PostSerializer
from .models import Post
from django.conf.urls import url


def post_list(request):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    json_utf8_string = JSONRenderer().render(serializer.data)
    return HttpResponse(json_utf8_string, content_type='application/json',
                        charset='utf-8')


urlpatterns = [
    url(r'^post/list/$',post_list, name='api_v1_post_list')
]