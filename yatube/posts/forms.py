from django import forms
from .models import Post, Group


class PostForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'cols': '40', 'rows': '10'
    }))

    # group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=('Нет'), widget=forms.Select(attrs={
    #     'class': 'form-control'
    # }))
    class Meta:
        model = Post
        fields = ('text', 'group')
