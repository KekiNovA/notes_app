from django.urls import path
from .views import CreateNoteView, GetNoteView, ShareNoteView, NoteVersionView

urlpatterns = [
    path('create', CreateNoteView.as_view()),
    path('<int:pk>', GetNoteView.as_view()),
    path('share', ShareNoteView.as_view()),
    path('version-history/<int:note_id>', NoteVersionView.as_view()),
]
