from django.shortcuts import render, get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,\
UpdateView, CreateView
from .models import Post, Comment
from .forms import CommentModelForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.defaultfilters import truncatewords
# Create your views here.


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_post_list.html']
        return ['blog/index.html']


class ScrollListView(ListView):
    model = Post
    paginate_by = 10

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_scroll_list.html']
        return ['blog/scroll_list.html']


index = PostListView.as_view()

# def index(request):
#     return render(request, 'example/beyul_3.html')

scroll = ScrollListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_template_names(self):
        return ['blog/post_detail.html']

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse({
                'title': self.object.title,
                'summary': truncatewords(self.object.content, 20)
            })
        else:
            return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentModelForm()
        return context

post_detail = PostDetailView.as_view()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

post_delete = PostDeleteView.as_view()


class PostCreateView(CreateView):
    model = Post

post_new = PostCreateView.as_view(fields=['title', 'content'])


class PostEditView(UpdateView):
    model = Post

post_edit = PostEditView.as_view(fields=['title', 'content'])


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentModelForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        response = super().form_valid(form)
        if self.request.is_ajax():
            return render(self.request, 'blog/_comment_form.html',{
                'comment': comment
            })
        return response

    def get_success_url(self):
        return resolve_url(self.object.post)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_comment_form.html']
        return ['blog/comment_form.html']

comment_new = CommentCreateView.as_view(template_name='blog/comment_form.html')


class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(post__id=self.kwargs['post_pk']).all()
        return qs

comment_list = CommentListView.as_view()


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentModelForm

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.is_ajax():
            return render(self.request, 'blog/_comment.html', {
                'comment': self.object
            })
        return response

    def get_success_url(self):
        return resolve_url(self.object.post)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['blog/_comment_form.html']
        return ['blog/comment_form.html']

comment_edit = CommentUpdateView.as_view(template_name='blog/comment_form.html')


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_delete = CommentDeleteView.as_view()


def example(request):
    return render(request, 'example/homework.html')
