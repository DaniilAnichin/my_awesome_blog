from uuid import UUID

from django.conf import settings
from django.db import models

from my_awesome_blog.models import Model


class Post(Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    views = models.PositiveIntegerField(default=0, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='posts')

    def __str__(self):
        return self.title

    def set_tags(self, tags):
        for tag in tags:
            if isinstance(tag, Tag):
                self.tags.add(tag)
            if not isinstance(tag, str):
                continue
            try:
                tag = str(UUID(tag))
                self.tags.add(tag)
            except ValueError:
                self.tags.add(Tag.objects.get_or_create(name=tag)[0])

    def increment_views(self):
        self.views += 1
        Post.objects.filter(pk=self.pk).update(views=models.F('views') + 1)


class Tag(Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name
