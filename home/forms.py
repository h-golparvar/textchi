from django import forms
from .models import Comment, Song
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()


class SongEditForm(forms.ModelForm):
    template_name = "management/form_snippet.html"
    aaa = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'ckeditor'}))

    class Meta:
        model = Song
        fields = '__all__'
        exclude = ['writer']
        widgets = {
            'fa_name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'singer': forms.Select(attrs={'class': 'form-control'}),
            'lyric': forms.TextInput(attrs={'class': 'form-control ckeditor'}),
            'pine': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meta_description': forms.TextInput(attrs={'class': 'form-control'}),
            'noindex': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'canonical': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.TextInput(attrs={'class': 'form-control'}),
            'dl_128': forms.TextInput(attrs={'class': 'form-control'}),
            'dl_320': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'situation': forms.Select(attrs={'class': 'form-control'}),
        }
