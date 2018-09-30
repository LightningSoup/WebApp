from django.db import models
from django.contrib import admin
from datetime import datetime

# Resource object - The core model for uploaded content. Also depracated
class ResourceManager(models.Manager):
    def create_resource(self, name, title, hash, owner):
        resource = self.create(name=name, title=title, hash=hash, owner=owner, birthday=datetime.now())

        return resource


class Resource(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    hash = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    birthday = models.DateField()

    objects = ResourceManager()

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'birthday', 'hash')

class BlogManager(models.Manager):
    def create_blog(self, name, title, homepage_hash, owner, forkof=""):
        blog = self.create(name=name, title=title, homepage_hash=homepage_hash, owner=owner, birthday=datetime.now(), forkof=forkof)

        return blog

class Blog(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    homepage_hash = models.CharField(max_length=150)
    birthday = models.DateField()
    forkof = models.CharField(max_length=150)

    objects = BlogManager()

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'birthday', 'homepage_hash')

class PostManager(models.Manager):
    def create_post(self, name, title, hash, owner, blog="", forkof=""):
        post = self.create(name=name, title=title, hash=hash, owner=owner, birthday=datetime.now(), blog=blog, forkof=forkof)

        return post

class Post(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    hash = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    blog = models.CharField(max_length=150, default="")
    birthday = models.DateField()
    forkof = models.CharField(max_length=150)

    objects = PostManager()

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'blog', 'birthday', 'hash')

class RecipeManager(models.Manager):
    def create_recipe(self, name, title, hash, owner, fork_of=""):
        post = self.create(name=name, title=title, hash=hash, owner=owner, birthday=datetime.now(), fork_of=fork_of)

        return post

class Recipe(models.Manager):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    hash = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    fork_of = models.CharField(max_length=150, default="")
    birthday = models.DateField()

    objects = RecipeManager()
