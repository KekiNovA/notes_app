from rest_framework import serializers
from .models import Note, NoteLine, NoteVersion


class CreateNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = []


class NoteLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoteLine
        fields = ['line_number', 'content']
        order_by = 'line_number'


class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    lines = NoteLineSerializer(many=True)

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["lines"] = sorted(
            response["lines"], key=lambda x: x["line_number"])
        return response


class NoteVersionSerilizer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = NoteVersion
        fields = "__all__"
