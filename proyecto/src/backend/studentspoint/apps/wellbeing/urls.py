from django.urls import path

from .views import BienestarListView

urlpatterns = [path("bienestar/", BienestarListView.as_view(), name="bienestar")]
