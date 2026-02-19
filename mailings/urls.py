from django.urls import path
from .views import (
    MailingListView,
    MailingCreateView,
    MailingDetailView,
    MailingUpdateView,
    MailingDeleteView,
    MailingSendView,
    MailingReportView, MailingDisableView
)

app_name = 'mailings'

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),
    path("report/", MailingReportView.as_view(), name="mailing_report"),
    path("<int:pk>/disable/", MailingDisableView.as_view(), name="mailing_disable"),
]
