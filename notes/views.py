from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .permissions import IsNoteOwner, HasNoteAccess
from .models import Note, NoteSharedUsers
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


class ShareNoteView(APIView):
    permission_classes = [IsNoteOwner]

    def post(self, request):
        data = request.data
        note = Note.objects.get(pk=data['note_id'])
        usernames = request.data.get("usernames", [])
        print(usernames)
        if not usernames:
            raise ValidationError(
                {'error': 'Please provide usernames to share with.'})

        users = User.objects.filter(username__in=usernames)
        if len(users) != len(usernames):
            invalid_usernames = set(
                usernames) - set(users.values_list('username', flat=True))
            raise ValidationError(
                {'error': f"Invalid usernames: {', '.join(invalid_usernames)}"})
        if request.user.username in usernames:
            raise ValidationError({'error': 'You cannot share with yourself.'})

        mapping, created = NoteSharedUsers.objects.get_or_create(note=note)
        mapping.shared_users.add(*users)
        mapping.save()

        return Response({"message": "Note shared successfully."}, status=status.HTTP_200_OK)
