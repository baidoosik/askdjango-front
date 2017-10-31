from django.shortcuts import render, get_object_or_404, resolve_url
from django.views.generic import ListView, DetailView, UpdateView, DeleteView,\
UpdateView, CreateView
from .models import Post, Comment
from django.urls import reverse_lazy
# Create your views here.


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get_template_names(self):
        return ['blog/index.html']

index = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_template_names(self):
        return ['blog/post_detail.html']

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
    fields = ['message']

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_new = CommentCreateView.as_view(template_name='blog/comment_form.html')


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['message']

    def get_success_url(self):
        return resolve_url(self.object.post)
comment_edit = CommentUpdateView.as_view(template_name='blog/comment_form.html')


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return resolve_url(self.object.post)

comment_delete = CommentDeleteView.as_view()

def example(request):
    return render(request, 'example/homework.html')


