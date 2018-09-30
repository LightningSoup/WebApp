from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse

from .forms import CreateAccountForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .helper_fns import create_new_user
from knack.helper_fns import create_new_resource, create_new_blog, create_new_post, edit_post, edit_blog

from knack.forms import NewResourceForm, NewBlogForm, NewPostForm, EditPostForm, EditBlogForm

from knack.ipfs import cat

from knack.models import Resource, Blog, Post
from django.contrib import messages


class DescriptionPageView(TemplateView):
    template_name = "description.html"

class WebHostingPageView(TemplateView):
    template_name = "web_hosting.html"

class GettingStartedPageView(TemplateView):
     template_name = "getting_started.html"

def render_getting_started(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        create_form = CreateAccountForm(request.POST)
        login_form = LoginForm(request.POST)
        # check whether it's valid:
        if create_form.is_valid() and login_form.is_valid():
            # Ummm... the user clicked both submit buttons?
            # This person is totally a hacker.
            return HttpResponseRedirect('/thanks/')
        elif create_form.is_valid() and not login_form.is_valid():
            # User is creating a new user, and all form elements are present.
            userName = create_form.cleaned_data['create_name']
            userPass = create_form.cleaned_data['create_pswd']
            userEmail = create_form.cleaned_data['create_email']
            userPass_confirm = create_form.cleaned_data['create_confirm_pswd']
            userFName = create_form.cleaned_data['create_fname']

            # Check for password parity before creating the account
            if(userPass != userPass_confirm):
                # 'Password' and 'Confirm Password' fields don't match! Throw an error.
                messages.error(request, 'Passwords don\'t match!')
                return HttpResponseRedirect("/getting_started/")

            new_user = create_new_user(userName, userPass, first_name=userFName, email=userEmail)

            if(not new_user):
                # Create user account failed because the username is taken.
                # Redirect to getting_started with an error message.
                messages.error(request, 'Username \'%s\' is taken. Please choose another username.' %userName)
                return HttpResponseRedirect("/getting_started/")

            login(request, new_user)

            return HttpResponseRedirect('/user/' + userName + '/')
        elif not create_form.is_valid() and login_form.is_valid():
            username = login_form.cleaned_data['login_name']
            password = login_form.cleaned_data['login_pswd']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/user/' + user.username + '/')
            else:
                # Return an 'invalid login' error message.
                new_create_form = CreateAccountForm()
                new_login_form = LoginForm(initial={'login_name': username,
                                                    'login_pswd': password})

                messages.error(request, 'Incorrect password or account does not exist.')
                return HttpResponseRedirect('/getting_started/')

                #return render(request, 'getting_started.html', {'create_form': create_form, 'login_form': login_form})

    # if a GET (or any other method) we'll create a blank form
    else:
        create_form = CreateAccountForm()
        login_form = LoginForm()

    return render(request, 'getting_started.html', {'create_form': create_form, 'login_form': login_form})

def render_wysiwyg(request):
    return render(request, 'wysiwyg.html')

def render_how_it_works(request):
    return render(request, 'how_it_works.html')

def render_contribute(request):
    return render(request, 'contribute.html')

def render_test(request):
    return render(request, 'test.html', {})

class BlogDisplay():
    def __init__(self, blog, post_list):
        self.blog_obj = blog
        self.post_list = post_list

def render_user(request, username):
    user = User.objects.filter(username=username)[0]
    raw_blog_list = Blog.objects.filter(owner=username)
    post_list = {}
    for blog in raw_blog_list:
        post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

    blog_list = []
    for blog in raw_blog_list:
        blog_list.append(BlogDisplay(blog, post_list[blog.name]))

    return render(request, 'user.html', {'user':      user,
                                         'blog_list': blog_list})

def render_new_resource(request, username):
    if(request.method == "POST"):
        # Creating a new resource
        form = NewResourceForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new Resource
            rcs_name = form.cleaned_data['new_r_name']
            rcs_title = form.cleaned_data['new_r_title']
            rcs_contents = b''
            for chunk in request.FILES["file"].chunks():
                rcs_contents = rcs_contents + chunk
            create_new_resource(rcs_title, rcs_name, rcs_contents, username)
        return HttpResponseRedirect('/user/' + username + "/" + rcs_name + "/")
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        resource_list = Resource.objects.filter(owner=username)

        new_resource_form = NewResourceForm()

        return render(request, 'new_resource_form.html', {'user':          user,
                                                          'resource_list': resource_list,
                                                          'resource':      new_resource_form})

def render_new_blog(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        messages.error(request, 'Please log in as \'%s\' before creating a new blog.' %username)
        return HttpResponseRedirect("/getting_started/")
    if(request.method == "POST"):
        # Creating a new resource
        form = NewBlogForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new blog
            blog_name = form.cleaned_data['name']
            blog_title = form.cleaned_data['title']
            homepage_contents = b''
            for chunk in request.FILES["homepage"].chunks():
                homepage_contents = homepage_contents + chunk
            create_new_blog(blog_title, blog_name, homepage_contents, username)
            return HttpResponseRedirect('/user/' + username + "/" + blog_name)
        else:
            # Every username is unique, so we can assume that this user exists.
            # TODO: Error checking in case user does not exist
            user = User.objects.filter(username=username)[0]
            raw_blog_list = Blog.objects.filter(owner=username)
            post_list = {}
            for blog in raw_blog_list:
                post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

            blog_list = []
            for blog in raw_blog_list:
                blog_list.append(BlogDisplay(blog, post_list[blog.name]))

            new_blog_form = NewBlogForm()

            return render(request, 'new_blog_form.html', {'user': user,
                                                          'blog_list':     blog_list,
                                                          'resource':      new_blog_form})
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        raw_blog_list = Blog.objects.filter(owner=username)
        post_list = {}
        for blog in raw_blog_list:
            post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

        blog_list = []
        for blog in raw_blog_list:
            blog_list.append(BlogDisplay(blog, post_list[blog.name]))

        new_blog_form = NewBlogForm()

        return render(request, 'new_blog_form.html', {'user': user,
                                                      'blog_list':     blog_list,
                                                      'resource':      new_blog_form})

def render_new_post(request, username, blog_name):
    if not request.user.is_authenticated or request.user.username != username:
        messages.error(request, 'Please log in as \'%s\' before creating a new post.' %username)
        return HttpResponseRedirect("/getting_started/")
    if(request.method == "POST"):
        # Creating a new resource
        form = NewPostForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new blog
            post_name = form.cleaned_data['name']
            post_title = form.cleaned_data['title']
            page_contents = b''
            for chunk in request.FILES["homepage"].chunks():
                page_contents = page_contents + chunk
            create_new_post(post_title, post_name, page_contents, username, blog_name)
            return HttpResponseRedirect('/user/' + username + "/" + blog_name + "/" + post_name)
        else:
            # Every username is unique, so we can assume that this user exists.
            # TODO: Error checking in case user does not exist
            user = User.objects.filter(username=username)[0]
            raw_blog_list = Blog.objects.filter(owner=username)
            post_list = {}
            for blog in raw_blog_list:
                post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

            blog_list = []
            for blog in raw_blog_list:
                blog_list.append(BlogDisplay(blog, post_list[blog.name]))

            new_post_form = NewPostForm()

            return render(request, 'new_post_form.html', {'user': user,
                                                          'blog_list':     blog_list,
                                                          'resource':      new_blog_form})
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        raw_blog_list = Blog.objects.filter(owner=username)
        post_list = {}
        for blog in raw_blog_list:
            post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

        blog_list = []
        for blog in raw_blog_list:
            blog_list.append(BlogDisplay(blog, post_list[blog.name]))

        new_blog_form = NewPostForm()

        return render(request, 'new_post_form.html', {'user': user,
                                                      'blog_list':     blog_list,
                                                      'resource':      new_blog_form})

def render_resource(request, username, resourcename):
    if(request.method == "POST"):
        # This person is totally a hacker. Do something secure here
        return HttpResponseRedirect('/pee-is-stored-in-the-balls/')
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        resource = Resource.objects.filter(name=resourcename, owner=username)[0]

        resource_content = cat(resource.hash)

        return HttpResponse(resource_content)

def render_blog(request, username, blog_name):
    if(request.method == "POST"):
        # This person is totally a hacker. Do something secure here
        return HttpResponseRedirect('/pee-is-stored-in-the-balls/')
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        blog = Blog.objects.filter(name=blog_name, owner=username)[0]

        blog_content = cat(blog.homepage_hash)

        return HttpResponse(blog_content)

def render_edit_resource(request, username):
    if not request.user.is_authenticated or request.user.username != username:
        return HttpResponseRedirect("/getting_started/", {'error_message': 'please log in before making changes.'})
    if(request.method == "POST"):
        # Creating a new resource
        form = NewResourceForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new Resource
            rcs_name = form.cleaned_data['new_r_name']
            rcs_contents = b''
            for chunk in request.FILES["file"].chunks():
                rcs_contents = rcs_contents + chunk
            create_new_resource(rcs_name, rcs_contents)
        return HttpResponseRedirect('/create/')
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        resource_list = Resource.objects.filter(owner=username)

        new_resource_form = NewResourceForm()

        return render(request, 'new_resource_form.html', {'user':          user,
                                                          'resource_list': resource_list,
                                                          'resource':      new_resource_form})

def render_edit_blog(request, username, blog_name):
    if not request.user.is_authenticated or request.user.username != username:
        messages.error(request, 'Please log in as user \'%s\' before making changes.' %username)
        return HttpResponseRedirect("/getting_started/")
    if(request.method == "POST"):
        # Creating a new resource
        form = EditBlogForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new blog
            new_blog_name = form.cleaned_data['name']
            blog_title = form.cleaned_data['title']
            page_contents = b''
            if("homepage" in request.FILES):
                for chunk in request.FILES["homepage"].chunks():
                    page_contents = page_contents + chunk
                new_file = True
            else:
                new_file = False
            edit_blog(blog_name, blog_title, new_blog_name, page_contents, username, new_file)
            return HttpResponseRedirect('/user/' + username + "/" + new_blog_name + "/view/")
        else:
            # Every username is unique, so we can assume that this user exists.
            # TODO: Error checking in case user does not exist
            user = User.objects.filter(username=username)[0]
            raw_blog_list = Blog.objects.filter(owner=username)
            post_list = {}
            for blog in raw_blog_list:
                post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

            blog_to_edit = None

            blog_list = []
            for blog in raw_blog_list:
                blog_list.append(BlogDisplay(blog, post_list[blog.name]))
                if(blog.name == blog_name):
                    blog_to_edit = blog

            new_blog_form = EditBlogForm(initial={'title': blog_to_edit.title,
                                                  'name': blog_to_edit.name,
                                                  'owner': blog_to_edit.owner})


            return render(request, 'edit_blog_form.html', {'user': user,
                                                          'blog_list':     blog_list,
                                                          'resource':      new_blog_form,
                                                          'blog':          blog})
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        raw_blog_list = Blog.objects.filter(owner=username)
        post_list = {}
        for blog in raw_blog_list:
            post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

        blog_to_edit = None

        blog_list = []
        for blog in raw_blog_list:
            blog_list.append(BlogDisplay(blog, post_list[blog.name]))
            if(blog.name == blog_name):
                blog_to_edit = blog

        new_blog_form = EditBlogForm(initial={'title': blog_to_edit.title,
                                              'name': blog_to_edit.name,
                                              'owner': blog_to_edit.owner})


        return render(request, 'edit_blog_form.html', {'user': user,
                                                      'blog_list':     blog_list,
                                                      'resource':      new_blog_form,
                                                      'blog':          blog})

def render_post(request, username, blog_name, post_name):
    if(request.method == "POST"):
        # This person is totally a hacker. Do something secure here
        return HttpResponseRedirect('/pee-is-stored-in-the-balls/')
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        post = Post.objects.filter(blog=blog_name, owner=username, name=post_name)[0]

        post_content = cat(post.hash)

        return HttpResponse(post_content)

def render_view_blog(request, username, blog_name):
    # Every username is unique, so we can assume that this user exists.
    # TODO: Error checking in case user does not exist
    user = User.objects.filter(username=username)[0]
    raw_blog_list = Blog.objects.filter(owner=username)
    post_list = {}
    for blog in raw_blog_list:
        post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

    blog_to_view = None

    blog_list = []
    for blog in raw_blog_list:
        blog_list.append(BlogDisplay(blog, post_list[blog.name]))
        if(blog.name == blog_name):
            blog_to_view = blog


    return render(request, 'view_blog.html', {'user': user,
                                                  'blog_list':     blog_list,
                                                  'blog':          blog_to_view})

def render_view_post(request, username, blog_name, post_name):
    # Every username is unique, so we can assume that this user exists.
    # TODO: Error checking in case user does not exist
    user = User.objects.filter(username=username)[0]
    raw_blog_list = Blog.objects.filter(owner=username)
    post_list = {}
    for blog in raw_blog_list:
        post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

    post = None

    blog_list = []
    for blog in raw_blog_list:
        blog_list.append(BlogDisplay(blog, post_list[blog.name]))
        if(blog.name == blog_name):
            post = [x for x in post_list[blog_name] if x.name == post_name][0]


    new_blog_form = NewPostForm()


    return render(request, 'view_post.html', {'user': user,
                                                  'blog_list':     blog_list,
                                                  'resource':      new_blog_form,
                                                  'post':          post})

def render_edit_post(request, username, blog_name, post_name):
    if not request.user.is_authenticated or request.user.username != username:
        messages.error(request, 'Please log in as user \'%s\' before making changes.' %username)
        return HttpResponseRedirect("/getting_started/")
    if(request.method == "POST"):
        # Creating a new resource
        form = EditPostForm(request.POST, request.FILES)
        if(form.is_valid()):
            # Create a new blog
            new_post_name = form.cleaned_data['name']
            post_title = form.cleaned_data['title']
            page_contents = b''
            if("homepage" in request.FILES):
                for chunk in request.FILES["homepage"].chunks():
                    page_contents = page_contents + chunk
                new_file = True
            else:
                new_file = False
            edit_post(post_name, post_title, new_post_name, page_contents, username, blog_name, new_file)
            return HttpResponseRedirect('/user/' + username + "/" + blog_name + "/" + new_post_name +  "/view/")
        else:
            # Every username is unique, so we can assume that this user exists.
            # TODO: Error checking in case user does not exist
            user = User.objects.filter(username=username)[0]
            raw_blog_list = Blog.objects.filter(owner=username)
            post_list = {}
            for blog in raw_blog_list:
                post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

            post = None

            blog_list = []
            for blog in raw_blog_list:
                blog_list.append(BlogDisplay(blog, post_list[blog.name]))
                if(blog.name == blog_name):
                    post = [x for x in post_list[blog_name] if x.name == post_name][0]


            new_blog_form = EditPostForm(initial={'title': post.title,
                                                  'name': post.name,
                                                  'blog': post.blog,
                                                  'owner': post.owner})


            return render(request, 'edit_post_form.html', {'user': user,
                                                          'blog_list':     blog_list,
                                                          'resource':      new_blog_form,
                                                          'post':          post})
    else:
        # Every username is unique, so we can assume that this user exists.
        # TODO: Error checking in case user does not exist
        user = User.objects.filter(username=username)[0]
        raw_blog_list = Blog.objects.filter(owner=username)
        post_list = {}
        for blog in raw_blog_list:
            post_list[blog.name] = Post.objects.filter(blog=blog.name, owner=username)

        post = None

        blog_list = []
        for blog in raw_blog_list:
            blog_list.append(BlogDisplay(blog, post_list[blog.name]))
            if(blog.name == blog_name):
                post = [x for x in post_list[blog_name] if x.name == post_name][0]


        new_blog_form = EditPostForm(initial={'title': post.title,
                                              'name': post.name,
                                              'blog': post.blog,
                                              'owner': post.owner})


        return render(request, 'edit_post_form.html', {'user': user,
                                                      'blog_list':     blog_list,
                                                      'resource':      new_blog_form,
                                                      'post':          post})

def render_fork_blog(request, username, blog_name):
    if(request.user.is_authenticated):
        # Creating a fork of the blog
        blog_to_fork = Blog.objects.filter(owner=username, name=blog_name)[0]
        name = blog_to_fork.name
        title = blog_to_fork.title
        owner = request.user.username
        homepage_hash = blog_to_fork.homepage_hash
        forkof = blog_to_fork.name
        new_blog = create_new_blog(title, name, "", owner, forkof=forkof, homepage_hash=homepage_hash)

        # Redirecting to the forked version
        return HttpResponseRedirect("/user/" + request.user.username + "/" + blog_name + "/view/")
    else:
        messages.error(request, 'Please log in before forking.')
        return HttpResponseRedirect("/getting_started/")

def render_fork_post(request, username, blog_name, post_name):
    if(request.method == "GET" and request.user.is_authenticated):
        # Creating a fork of the post
        post_to_fork = Post.objects.filter(owner=username, blog=blog_name, name=post_name)[0]
        name = post_to_fork.name
        title = post_to_fork.title
        owner = request.user.username
        homepage_hash = post_to_fork.hash
        forkof = post_to_fork.name
        new_post = create_new_post(title, name, "", owner, blog_name, forkof=forkof, homepage_hash=homepage_hash)

        # Redirecting to the forked version
        return HttpResponseRedirect("/user/" + request.user.username + "/" + blog_name + "/" + post_name + "/view/")

        return render(request, 'view_post.html', {'user': request.user,
                                                      'blog_list':     blog_list,
                                                      'resource':      new_blog_form,
                                                      'post':          new_post})
    else:
        messages.error(request, 'Please log in before forking.')
        return HttpResponseRedirect("/getting_started/")
