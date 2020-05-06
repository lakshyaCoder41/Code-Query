from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.
# Below Post model is our Query entity
class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)#default arg means we can change datetime also whenever user wanted
    image=models.ImageField(blank=True,null=True,upload_to='post_pics')
    author= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # overriding the parent class method save to add some different functionality
        super(Post, self).save(*args, **kwargs)
        if self.image:
            img=Image.open(self.image.path)

            #resizing image if a user uploaded large size profile pic
            if img.height>400 or img.width>400:
                output_size=(400,400)
                img.thumbnail(output_size)
                img.save(self.image.path)

#redirect() will take to specific url but reverse() just takes one step back of the url
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',null=True)
    author= models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    vote=models.IntegerField(default=0)
    image=models.ImageField(upload_to='comment_pics',blank=True,null=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        # overriding the parent class method save to add some different functionality
        super(Comment, self).save(*args, **kwargs)
        if self.image:
            img=Image.open(self.image.path)

        #resizing image if a user uploaded large size profile pic
            if img.height>400 or img.width>400:
                output_size=(400,400)
                img.thumbnail(output_size)
                img.save(self.image.path)


    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.post.pk})



class UserCommentVote(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote=models.IntegerField(default=0)
