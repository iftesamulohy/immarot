from django.contrib import admin

from books.models import Author, Book, Dummy, Mykey, Mykey2, YourModel

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Dummy)
admin.site.register(YourModel)
admin.site.register(Mykey)
admin.site.register(Mykey2)