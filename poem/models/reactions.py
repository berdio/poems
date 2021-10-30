from django.db import models
from django.contrib.auth.models import User

from .poem import Poem


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'poem')


class Like(Reaction):
    def save(self, *args, **kwargs) -> None:
        self.poem.dislike_set.filter(user=self.user).delete()
        return super().save(*args, **kwargs)


class Dislike(Reaction):
    def save(self, *args, **kwargs) -> None:
        self.poem.like_set.filter(user=self.user).delete()
        return super().save(*args, **kwargs)


class Comment(Reaction):
    text = models.TextField()

    class Meta:
        pass
