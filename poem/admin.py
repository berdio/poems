from django.contrib import admin

from .models import Author, Poem, Like, Dislike, Comment


admin.site.register(Author)
admin.site.register(Poem)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
