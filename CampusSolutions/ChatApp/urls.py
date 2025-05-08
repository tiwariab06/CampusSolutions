# messaging/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("faculties/", views.get_faculties, name="get_faculties"),
    path("students/", views.get_studentschatapp, name="get_studentschatapp"),
    path("faculties/chat/<int:user_id>/", views.message, name="message"),
    path("students/chat/<int:user_id>/", views.message, name="message"),
    path("students/chatbox/<int:user_id>/", views.chatbox, name="chatbox"),
    path("faculties/chatbox/<int:user_id>/", views.chatbox, name="chatbox"),
    path(
        "students/get-messages/<int:user_id>/", views.get_messages, name="get_messages"
    ),
    path(
        "faculties/get-messages/<int:user_id>/", views.get_messages, name="get_messages"
    ),
    # path(
    #     "conversation/start/<int:user_id>/",
    #     views.start_conversation,
    #     name="start_conversation",
    # ),
    # path("conversation/<int:conversation_id>/", views.chat_room, name="chat_room"),
    # path(
    #     "conversation/<int:conversation_id>/send/",
    #     views.send_message,
    #     name="send_message",
    # ),
]
