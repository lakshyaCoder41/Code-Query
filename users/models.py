from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from blog.models import Post

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # overriding the parent class method save to add some different functionality
        super(Profile, self).save(*args, **kwargs)

        img=Image.open(self.image.path)

        #resizing image if a user uploaded large size profile pic
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
