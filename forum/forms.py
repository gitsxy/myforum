from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="ConfPassword", widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class AddPostForm(forms.Form):
    title = forms.CharField(label="Title")
    context = forms.CharField(label="Context")

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class PostForm(forms.Form):
    #choice = forms.ChoiceField(label='topic',choices=[(1,'a'),(2,'b'),(3,'c'),(4,'d')])
    #title = forms.CharField(label='Title')
    context = forms.CharField(widget=SummernoteWidget())

class ReplyForm(forms.Form):
    context = forms.CharField(widget=SummernoteWidget())

class EditProfileForm(forms.Form):
    nickname = forms.CharField(label='Nickname')
    sex = forms.ChoiceField(label='Sex',choices=[(1,'Male'),(2,'Famale')])
    signature = forms.CharField(label='Signature')

    