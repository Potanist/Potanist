from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    class Meta:
        ordering = ['-cre_date']

    cre_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title

