from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed, name='home_feed'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('share/<int:post_id>/', views.share_post, name='share_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/add/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('search/', views.search_users, name='search_users'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('report/<int:user_id>/', views.report_user, name='report_user'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
]