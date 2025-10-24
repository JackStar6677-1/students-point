from django.urls import path

from .views import (
    PushSubscribeView, 
    PushTestView, 
    get_notifications, 
    mark_notification_read, 
    mark_all_notifications_read
)

urlpatterns = [
    path("notifications/push/subscribe", PushSubscribeView.as_view()),
    path("notifications/push/test", PushTestView.as_view()),
    path("notifications/", get_notifications, name="notifications-list"),
    path("notifications/<int:notification_id>/read", mark_notification_read, name="notification-read"),
    path("notifications/mark-all-read", mark_all_notifications_read, name="notifications-mark-all-read"),
]
