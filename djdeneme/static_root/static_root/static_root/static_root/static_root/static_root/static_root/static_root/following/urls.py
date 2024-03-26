from django.urls import path, re_path
from .views import user_follow_unfollow, follower_and_followed_list, modal_user_follow_unfollow

urlpatterns = [
    path("takip-sistemi", user_follow_unfollow, name='follow-unfollow'),
    path("modal-takip-sistemi/", modal_user_follow_unfollow, name='modal-follow-unfollow'),
    re_path(r'^(?P<follow_type>[\w-]+)/$', follower_and_followed_list, name='follower-followed-list'),


]
