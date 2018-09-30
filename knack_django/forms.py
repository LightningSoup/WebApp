from django import forms

class CreateAccountForm(forms.Form):
    create_fname = forms.CharField(label='Name', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Jack Sparrow',
                                                              'class':       'text-input',
                                                              'size':        '50%'}))
    create_name = forms.CharField(label='Username', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'yisdarumgone',
                                                              'class':       'text-input',
                                                              'size':        '50%'}))
    create_email = forms.CharField(label='Email', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'We won\'t use it now, but maybe later',
                                                              'class':       'text-input',
                                                              'size':        '50%'}))
    create_pswd = forms.CharField(label='Password', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': '"password" is not a good password.',
                                                              'class':       'text-input',
                                                              'size':        '50%',
                                                              'type':        'password'}))
    create_confirm_pswd = forms.CharField(label='Confirm Password', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'Okay to reuse your password here. Nowhere else.',
                                                              'class':       'text-input',
                                                              'size':        '50%',
                                                              'type':        'password'}))

class LoginForm(forms.Form):
    login_name = forms.CharField(label='Username', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': 'BilboMcSwaggins',
                                                              'class':       'text-input',
                                                              'size':        '50%'}))
    login_pswd = forms.CharField(label='Password', max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "passwords aren't paper. Don't recycle them.",
                                                              'class':       'text-input',
                                                              'size':        '50%',
                                                              'type':        'password'}))
