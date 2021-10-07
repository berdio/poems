from django.contrib import admin

from .models import Author, Poem


admin.site.register(Author)
admin.site.register(Poem)