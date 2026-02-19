from django.urls import path
from .views import MessageListView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView

app_name = 'mail_messages'

urlpatterns = [path('', MessageListView.as_view(), name='message_list'),
               path('create/', MessageCreateView.as_view(), name='message_create'),
               path('<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
               path('<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
               path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'), ]
