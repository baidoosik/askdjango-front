from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .serializers import PostSerializer
from .models import Post
from django.conf.urls import url
from django.views.generic import ListView


# def post_list(request):
#     qs = Post.objects.all()
#     serializer = PostSerializer(qs, many=True)
#     json_utf8_string = JSONRenderer().render(serializer.data)
#     return HttpResponse(json_utf8_string, content_type='application/json',
#                         charset='utf-8')
class PostListView(ListView):
    def render_to_response(self, context):
        # ajax 요청이 아니면 템플릿 응답을 하고
        if not self.request.is_ajax():
            return super().render_to_response(context)
        # ajax 요청일 경우에는 json 응답을 하겠습니다
        qs = context['post_list']
        serializer = PostSerializer(qs, many=True)
        json_utf8_strging = JSONRenderer().render(serializer.data)
        return HttpResponse(json_utf8_strging,
                            content_type='application/json; charset=utf8')


urlpatterns = [
    # url(r'^post/list/$',post_list, name='api_v1_post_list')
]