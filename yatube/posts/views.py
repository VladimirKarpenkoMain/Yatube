from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView
from core.views import PostsBaseListView
from posts.models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

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


class GroupListView(PostsBaseListView):
    title = 'Здесь будет информация о группах проекта Yatube'

    def get_queryset(self):
        queryset = super(PostsBaseListView, self).get_queryset()
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        if group:
            queryset = Post.objects.filter(group=group).order_by('-pub_date')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsBaseListView, self).get_context_data()
        context['group'] = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        return context


class FollowView(PostsBaseListView):
    title = 'Избранное'

    def get_queryset(self):
        queryset = super(FollowView, self).get_queryset()
        following = self.request.user.following
        print(following)
        return queryset


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
        print(self.request.user.follower)
        context['accept'] = True if self.object == self.request.user else False
        context['following'] = True if self.object in self.request.user.following.all() else False
        return context


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['count'] = User.objects.get(id=self.object.author_id).posts.count()
        context['accept'] = True if self.object.author == self.request.user else False
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post_id=self.object.id)
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

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'post_id': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.is_authenticated:
            if self.object.author == self.request.user:
                return super(PostUpdateView, self).get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(f'/posts/{self.object.id}')
        else:
            return HttpResponseRedirect(f'/auth/login/')


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def profile_follow(request, username):
    Follow.objects.create(user=request.user, author=User.objects.get(username=username)).save()
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    Follow.objects.get(user=request.user, author=User.objects.get(username=username)).delete()
    return redirect('posts:profile', username=username)
