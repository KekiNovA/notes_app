from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsNoteOwner, HasNoteAccess
from .models import Note
from .serializers import CreateNoteSerializer, NoteSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateNoteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateNoteSerializer

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        return instance

    def create(self, request, *args, **kwargs):
        response = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = NoteSerializer(self.perform_create(serializer))
        response['message'] = 'Note created successfully'
        response['data'] = instance.data
        return Response(data=response, status=status.HTTP_201_CREATED)


class GetNoteView(RetrieveAPIView):
    permission_classes = [HasNoteAccess]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
