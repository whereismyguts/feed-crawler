from django.contrib import admin
from .models import Author, Post, Tag

def make_raw(modeladmin, request, posts):
    for p in posts:
        p.is_raw = True
        p.save()
        print("%s is raw again" % p)
class PostAdmin(admin.ModelAdmin):
    #list_display = ('title', 'address', 'port')
    actions = [make_raw]
    
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)