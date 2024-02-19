from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .permissions import IsNoteOwner, HasNoteAccess
from .models import Note, NoteSharedUsers, NoteLine, NoteVersion
from .serializers import CreateNoteSerializer, NoteSerializer, NoteVersionSerilizer
from django.contrib.auth import get_user_model
from django.db.models import F


User = get_user_model()


@swagger_auto_schema(request_body=CreateNoteSerializer,
                     responses={
                         201: '''Note created successfully''',
                         401: '''Unauthorized''',
                         500: '''Internal Server Error'''
                     })
class CreateNoteView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateNoteSerializer

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        return instance

    def create(self, request, *args, **kwargs):
        response = {}
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        lines = request.data.get('note_lines', [])
        if lines:
            current_line_number = 1
            for content in lines:
                NoteLine.objects.create(
                    note=instance,
                    line_number=current_line_number,
                    content=content,
                    created_by=request.user,
                    updated_by=request.user
                )
                current_line_number += 1
            content = NoteLine.objects.filter(
                note=instance).order_by('line_number').values('line_number', 'content')
            NoteVersion.objects.create(
                note=instance, content=list(content), created_by=request.user, status='CREATED')
        response['message'] = 'Note created successfully'
        response['data'] = NoteSerializer(instance).data
        return Response(data=response, status=status.HTTP_201_CREATED)


class GetNoteView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, HasNoteAccess]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    @swagger_auto_schema(request_body=NoteSerializer,
                         responses={
                             201: '''Note created successfully''',
                             401: '''Unauthorized''',
                             500: '''Internal Server Error'''
                         })
    def put(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            try:
                lines = request.data.get('lines', [])
                if lines:
                    formatted_lines = [
                        (int(line['line_number']), line['content']) for line in lines]
                else:
                    return Response({'error': f"Please provide lines"}, status=400)
            except (TypeError, KeyError) as e:
                return Response({'error': f"Invalid line data format: {e}"}, status=400)
            sorted_lines = sorted(formatted_lines, key=lambda x: x[0])

            existing_lines = {
                line.line_number: line for line in note.lines.all()}
            grouped_lines = {}
            for line_number, content in sorted_lines:
                group = 'new' if line_number not in existing_lines else 'existing'
                grouped_lines.setdefault(group, []).append(
                    (line_number, content))

            max_line_number = max(existing_lines.keys()
                                  ) if existing_lines else 0
            for line_number, content in grouped_lines.get('new', []):
                max_line_number += 1
                NoteLine.objects.create(
                    note=note,
                    line_number=max_line_number,
                    content=content,
                    created_by=request.user,
                    updated_by=request.user
                )

            if grouped_lines.get('existing', []):
                for obj in NoteLine.objects.filter(note=note, line_number__gte=line_number).order_by('-line_number'):
                    obj.line_number = F('line_number') + 1
                    obj.updated_by = request.user
                    obj.save()
                NoteLine.objects.create(
                    note=note,
                    line_number=line_number,
                    content=content,
                    created_by=request.user,
                    updated_by=request.user
                )
            content = NoteLine.objects.filter(
                note=note).order_by('line_number').values('line_number', 'content')
            NoteVersion.objects.create(
                note=note, content=list(content), created_by=request.user, status='UPDATED')
            return Response({'message': 'Lines updated successfully'}, status=200)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=404)
        except ValidationError as e:
            return Response({'error': e.detail}, status=400)


class ShareNoteView(APIView):
    permission_classes = [IsAuthenticated, IsNoteOwner]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'usernames': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='string'),
            },
            required=['usernames']
        ),
        responses={
            201: '''Note created successfully''',
            401: '''Unauthorized''',
            500: '''Internal Server Error'''
        })
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


@swagger_auto_schema(request_body=NoteVersionSerilizer,
                     responses={
                         201: '''Note created successfully''',
                         401: '''Unauthorized''',
                         500: '''Internal Server Error'''
                     })
class NoteVersionView(ListAPIView):
    permission_classes = [IsAuthenticated, IsNoteOwner]
    serializer_class = NoteVersionSerilizer

    def get_queryset(self):
        return NoteVersion.objects.filter(note__id=self.kwargs["note_id"])
