from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length = 120, null = True)
    value = models.CharField(max_length = 120, null=True)
    def __repr__(self):
        return "%s(%s)" %(self.name, self.value)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length = 250)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length = 320)
    html = models.TextField(null= True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, models.SET_NULL, blank=True, null=True)
    post_date = models.DateField(null =True)

    first_image = models.URLField(null = True)
    first_text = models.TextField(null= True)

    original_url = models.URLField(null = True)
    is_raw = models.BooleanField(default = True)

    def __str__(self):
        if self.title:
            return "%s by %s" % (self.title, self.author)
        return self.original_url

    