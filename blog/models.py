from django.db import models
from ckeditor.fields import RichTextField
from management.models import User
from django.urls import reverse


class MetaData(models.Model):
    title = models.CharField(max_length=300)
    body = RichTextField()
    picture = models.CharField(max_length=600, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    meta_title = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.CharField(max_length=200, null=True, blank=True)
    noindex = models.BooleanField(default=False)
    canonical = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(MetaData):
    is_sub = models.BooleanField(default=False)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub', blank=True, null=True)

    def get_absolute_url(self):
        return self.slug


class Tag(MetaData):

    def get_absolute_url(self):
        return self.slug


class Post(MetaData):
    category = models.ManyToManyField(Category, related_name='posts')
    tag = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created = models.DateTimeField(auto_now=True)
    CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Pending Review', 'Pending'),
    )
    situation = models.CharField(choices=CHOICES, max_length=14, default='Draft')
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')

    def get_absolute_url(self):
        return reverse('blog:blog-post', args=[self.slug])


class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = RichTextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    CHOICES = (
        ('Published', 'Published'),
        ('Draft', 'Draft'),
        ('Pending Review', 'Pending'),
    )
    situation = models.CharField(max_length=14, choices=CHOICES, default='Draft')

    replay = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replays')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} در {self.post}'

    @property
    def is_replay(self):
        if not self.replay:
            return False
        else:
            return True

