from django import forms
from .models import User
from home.models import Genre, Album
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValueError('passwords are not match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'picture', 'phone_number', 'email', 'password', 'is_admin', 'last_login']


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'password']


class GenerEditForm(forms.ModelForm):
    template_name = "management/form_snippet.html"

    class Meta:
        model = Genre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control h-auto'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
            'is_sub': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'sub_genre': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),

        }


class AddAlbumForm(forms.ModelForm):
    template_name = "management/form_snippet.html"

    class Meta:
        model = Album
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'singer': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.TextInput(attrs={'class': 'form-control'}),
            'pic': forms.FileInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),

            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control'}),
            'noindex': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'canonical': forms.TextInput(attrs={'class': 'form-control'}),
        }
