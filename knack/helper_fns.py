from .models import Resource, Blog, Post
from knack.ipfs import add_string, add_file_contents

def create_new_resource(resource_title, resource_name, contents, username):
    # contents is a bytearray, so cast it to a string
    hash = add_file_contents(contents)

    resource = Resource.objects.create_resource(resource_name, resource_title,
                         hash,
                         username)
    return resource

def create_new_blog(blog_title, blog_name, homepage, username, forkof="", homepage_hash=""):
    # contents is a bytearray, so cast it to a string
    if(homepage != ""):
        hash = add_file_contents(homepage)
    else:
        hash = homepage_hash

    blog = Blog.objects.create_blog(blog_name, blog_title,
                         hash, username, forkof)
    return blog

def create_new_post(post_title, post_name, homepage, username, blog_name, forkof="", homepage_hash=""):
    # contents is a bytearray, so cast it to a string
    if(homepage != ""):
        hash = add_file_contents(homepage)
    else:
        hash = homepage_hash

    post = Post.objects.create_post(post_name, post_title,
                         hash, username, blog_name, forkof)
    return post

def edit_post(old_name, post_title, post_name, homepage, username, blog_name, new_file):
    if(new_file):
        # contents is a bytearray, so cast it to a string
        hash = add_file_contents(homepage)

        post = Post.objects.filter(name=old_name)[0]
        post.title = post_title
        post.name = post_name
        post.hash = hash
        post.owner = username
        post.blog = blog_name
        post.save()
        return post
    else:
        post = Post.objects.filter(name=old_name)[0]
        post.title = post_title
        post.name = post_name
        post.owner = username
        post.blog = blog_name
        post.save()
        return post

def edit_blog(old_name, blog_title, blog_name, homepage, username, new_file):
    if(new_file):
        # contents is a bytearray, so cast it to a string
        hash = add_file_contents(homepage)

        blog = Blog.objects.filter(name=old_name)[0]
        blog.title = blog_title
        blog.name = blog_name
        blog.hash = hash
        blog.owner = username
        blog.save()
        return blog
    else:
        blog = Blog.objects.filter(name=old_name)[0]
        blog.title = blog_title
        blog.name = blog_name
        blog.owner = username
        blog.save()
        return blog
