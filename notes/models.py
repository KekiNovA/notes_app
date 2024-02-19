from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Note(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by.get_username()}"


class NoteSharedUsers(models.Model):
    note = models.OneToOneField(
        Note, on_delete=models.PROTECT)
    shared_users = models.ManyToManyField(
        User, related_name="shared_users", blank=True)

    def __str__(self):
        return f"{self.note.id}"


class NoteLine(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.PROTECT, related_name='lines')
    line_number = models.IntegerField()
    content = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"NoteLine (note: {self.note.id}, line: {self.line_number}, content: {self.content[:20]}...)"

    class Meta:
        unique_together = ('note', 'line_number',)


class NoteVersion(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.PROTECT, related_name='versions')
    content = models.JSONField()
    status = models.CharField(max_length=16, choices=[(
        'CREATED', 'CREATED'), ('UPDATED', 'UPDATED')])
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.note.id} - {self.created_by.get_username()}"
