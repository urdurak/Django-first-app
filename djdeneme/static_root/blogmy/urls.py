from django.urls import path, re_path
from .views import post_list, post_create, post_delete, post_update, post_detail,add_comment , add_or_remove_favorite

urlpatterns = [
    path("", post_list, name='post-list'),
    re_path('post_create/', post_create, name="post-create"),
    re_path(r'^post_detail/(?P<slug>[\w-]+)/$', post_detail, name="post-detail"),
    re_path(r'^post_update/(?P<slug>[\w-]+)/$', post_update, name="post-update"),
    re_path(r'^post_delete/(?P<slug>[\w-]+)/$', post_delete, name="post-delete"),
    re_path(r'^add_comment/(?P<slug>[\w-]+)/$', add_comment, name="add-comment"),
    re_path(r'^add_remove_favorite/(?P<slug>[\w-]+)/$', add_or_remove_favorite, name="add-remove-favorite"),

]
