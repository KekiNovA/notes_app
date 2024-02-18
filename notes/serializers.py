from rest_framework import serializers
from .models import Note


class CreateNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['title']


class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Note
        fields = '__all__'
