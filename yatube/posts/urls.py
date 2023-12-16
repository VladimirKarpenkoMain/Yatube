from django.urls import path

from . import views

from django.contrib.auth.decorators import login_required

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('groups/<slug:slug>/', views.GroupListView.as_view(), name='groups'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', login_required(views.PostCreateView.as_view()), name='create'),
    path('posts/<int:post_id>/edit/', login_required(views.PostUpdateView.as_view()), name='update'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('follow/', views.FollowView.as_view(), name='follow_index'),
    path('profile/<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('profile/<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow')
]