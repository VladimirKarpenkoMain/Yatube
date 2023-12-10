from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView
from posts.models import Post, Group
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.urls import reverse_lazy

User = get_user_model()


def index(request):
    template = 'posts/index.html'

    posts = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная страница',
        'page_obj': page_obj,
    }
    return render(request, template, context=context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Здесь будет информация о группах проекта Yatube',
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context=context)


class ProfileView(DetailView):
    template_name = 'posts/profile.html'
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        posts = Post.objects.filter(author=self.object).order_by('-pub_date')
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super(ProfileView, self).get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['count'] = self.object.posts.count()
        return context


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['count'] = User.objects.get(id=self.object.author_id).posts.count()
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/create_post.html'
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    success_url = reverse_lazy('posts:index')

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['is_edit'] = True
        return context
