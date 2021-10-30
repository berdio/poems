from django.db import models

from .author import Author


class Poem(models.Model):
    name = models.CharField(max_length=150, null=False)
    text = models.TextField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.author} - {self.name}'
