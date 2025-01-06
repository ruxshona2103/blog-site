from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class PublishedManager(models.Model):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status = 'publish')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogapp")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ("-publish", )

    def __str__(self):
        return self.title

    objects = models.Manager
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse("blog:post_detail", args= [self.publish.unique_for_year,
                                                        self.publish.month,
                                                        self.publish.day,
                                                        self.publish.slug])

posts = Post.objects.filter(status = "published")


