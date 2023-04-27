from django.db import models
from django.conf import settings
from django.db.models import Sum

from . import TYPE_CHOICES


class Author(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(default=0)

    def update_rating(self):
        my_posts = self.posts.all()
        post_comments = [p.post_comments.aggregate(sum=Sum('rating'))['sum'] for p in my_posts]
        post_comments = sum(post_comments)
        posts = self.posts.values('rating')
        posts = sum(p['rating'] for p in posts) * 3
        comments = self.user.comments.values('rating')
        comments = sum(c['rating'] for c in comments)
        self.rating = posts + comments + post_comments

class Category(models.Model):
    name = models.CharField(unique=True, max_length=256)
    subscribers = models.TextField(blank=True, null=True)

    def get_subscribers(self):
        return self.subscribers.split(';')
    def add_subscriber(self,email):
        if self.subscribers:
            s = self.subscribers.split(';')
            s.append(email)
            self.subscribers = ';'.join(s)
        else:
            self.subscribers = email
class Post(models.Model):
    author = models.ForeignKey(
        Author, related_name='posts',
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(Category)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    title = models.CharField(unique=True, max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text



    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1





class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='post_comments' )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
