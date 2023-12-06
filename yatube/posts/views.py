from django.shortcuts import render, get_object_or_404

from .models import Post, Group


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    # В словаре context отправляем информацию в шаблон
    context = {
        'title': 'Главная страница',
        'posts': posts,
    }
    return render(request, template, context=context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    context = {
        'title': 'Здесь будет информация о группах проекта Yatube',
        'posts': Post.objects.filter(group=group).order_by('-pub_date'),
        'group': group,
    }
    return render(request, template, context=context)
