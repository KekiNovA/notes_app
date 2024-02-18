from django.urls import path
from .views import CreateNoteView, GetNoteView

urlpatterns = [
    path('create', CreateNoteView.as_view()),
    path('<int:pk>', GetNoteView.as_view()),
]
