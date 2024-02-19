from django.contrib import admin
from .models import Note, NoteSharedUsers, NoteLine, NoteVersion

# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Note, NoteAdmin)
admin.site.register(NoteSharedUsers)
admin.site.register(NoteLine)
admin.site.register(NoteVersion)
