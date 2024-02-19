from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Note, NoteLine, NoteVersion
from .serializers import CreateNoteSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CreateNoteViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password")
        response = self.client.post(
            "/login", data={'username': 'test_user', 'password': 'test_password'}, format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {response.data['token']}")

    def test_create_note_success(self):
        data = {
            'title': 'Test Note',
            'content': 'Some initial content',
            'note_lines': ['Line 1', 'Line 2']
        }
        response = self.client.post('/notes/create', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        serializer = CreateNoteSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())
        note = Note.objects.get(id=response.data['data']['id'])
        note_lines = NoteLine.objects.filter(note=note).order_by('line_number')
        self.assertEqual(note.created_by, self.user)
        self.assertListEqual(list(note_lines.values_list(
            'content', flat=True)), data['note_lines'])
