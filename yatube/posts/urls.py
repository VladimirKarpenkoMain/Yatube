from django.urls import path

from . import views

from django.contrib.auth.decorators import login_required

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('groups/<slug:slug>/', views.group_posts, name='groups'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create', login_required(views.PostCreateView.as_view()), name='create'),
    path('posts/<int:post_id>/edit', login_required(views.PostUpdateView.as_view()), name='update'),
]