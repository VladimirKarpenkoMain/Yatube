from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from posts.models import Post, Group


def page_not_found(request, exception):
    return render(request, 'core/404.html', context={'path': request.path}, status=404)


def server_error(request):
    return render(request, 'core/500.html', context={'path': request.path}, status=500)


def permission_denied_view(request, exception):
    return render(request, 'core/403.html', context={'path': request.path}, status=403)


class PostsBaseListView(ListView):
    template_name = 'posts/group_list.html'
    model = Post
    paginate_by = 10
    title = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsBaseListView, self).get_context_data()
        context['title'] = self.title
        return context

