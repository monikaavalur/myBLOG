from django import forms
from .models import post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    content=forms.CharField(widget=PagedownWidget(show_preview=False))
    publish=forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model=post
        fields=[
            "title",
            "image",
            "content",
            "draft",
            "publish"
        ]