from django import forms

class NewResourceForm(forms.Form):
    new_r_name = forms.CharField(label='Resource URL', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': '/user/me/lolcats',
                                                              'class':       'text-input',
                                                              'size':        '30%'}))
    new_r_title = forms.CharField(label='Resource Title', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'LOL Cats',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    file = forms.FileField()

class NewBlogForm(forms.Form):
    title = forms.CharField(label='Blog Title', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Cooking with Pizzaz',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    name = forms.CharField(label='Blog URL', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'cooking-with-pizzaz',
                                                         'class':       'text-input',
                                                         'size':        '30%'}))
    homepage = forms.FileField()

class NewPostForm(forms.Form):
    title = forms.CharField(label='Post Title', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'Flooping',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    name = forms.CharField(label='Post URL', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'flooping',
                                                         'class':       'text-input',
                                                         'size':        '30%'}))
    homepage = forms.FileField()

class EditPostForm(forms.Form):
    title = forms.CharField(label='Post Title', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'post.title',
                                                                'id':        'title',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    name = forms.CharField(label='Post URL', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'post.name',
                                                         'id':        'name',
                                                         'class':       'text-input',
                                                         'size':        '30%'}))
    owner = forms.CharField(label='Post Owner', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'post.owner',
                                                                'id':        'owner',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    blog = forms.CharField(label='Blog', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'post.blog',
                                                         'id':        'blog',
                                                         'class':       'text-input',
                                                         'size':        '30%'}))
    homepage = forms.FileField(required=False)

class EditBlogForm(forms.Form):
    title = forms.CharField(label='Post Title', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'post.title',
                                                                'id':        'title',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    name = forms.CharField(label='Post URL', max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'post.name',
                                                         'id':        'name',
                                                         'class':       'text-input',
                                                         'size':        '30%'}))
    owner = forms.CharField(label='Post Owner', max_length=100,
                                  widget=forms.TextInput(attrs={'placeholder': 'post.owner',
                                                                'id':        'owner',
                                                                'class':       'text-input',
                                                                'size':        '30%'}))
    homepage = forms.FileField(required=False)
