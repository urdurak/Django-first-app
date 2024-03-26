from django.urls import path, re_path
from .views import inbox , personal_inbox , send_message

urlpatterns = [
    path("fbox/", inbox , name='chat-inbox'),
    re_path(r'^(?P<room_id>[\w-]+)/$', personal_inbox , name="personal-inbox"),
    re_path(r'^send-message/(?P<room_id>[\w-]+)/$', send_message , name="send_message"),
]
