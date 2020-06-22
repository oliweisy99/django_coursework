from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
User = get_user_model()
import misaka

class Blog(models.Model):
    user = models.ForeignKey(User, related_name='blog', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    content = models.TextField(max_length=4000)
    published_date = models.DateTimeField(auto_now=True)
    blog_pic = models.ImageField(upload_to='blog_pic',blank=True)
     
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = misaka.html(self.title)
        self.description = misaka.html(self.description)
        self.content = misaka.html(self.content)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk':self.pk})

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)


    class Meta:
        permissions = (("can_make_changes", "Can edit, Update or Delete content"),)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk':self.pk})

    def __str__(self):
        return self.text
    
    class Meta:
        permissions = (("can_make_decision", "Can approve or deny comments"),)

