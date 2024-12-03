from django.db import models

# Create your models here.
# models.py
from django.utils.text import slugify
from globalapp.models import Common

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    

    def __str__(self):
        return self.name

class Book(Common):
    title = models.CharField(max_length=200)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE,blank=True,null=True)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    image = models.ImageField(upload_to="images/",null=True,blank=True)

    def __str__(self):
        return self.title
    
class Dummy(models.Model):
    route = models.CharField(max_length=20,default=None)
    content = models.TextField(default=None)
    slug = models.SlugField(max_length=20, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a slug from the route field
            self.slug = slugify(self.route[:20])  # Use the first 50 characters of the route
        super(Dummy, self).save(*args, **kwargs)

class Mykey(models.Model):
    name = models.CharField(max_length=100)
    showable_fields = ['name']
    def __str__(self):
        return self.name
    
class Mykey2(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class YourModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key_name = models.ForeignKey(Mykey,on_delete=models.CASCADE,null=True,blank=True)
    key_name2 = models.ForeignKey(Mykey2,on_delete=models.CASCADE,null=True,blank=True)

    # Specify fields that are "showable"
    showable_fields = ['id','name', 'description','key_name','key_name2']
    def __str__(self):
        return self.name