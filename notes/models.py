from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by.get_username()}  - {self.title}"
