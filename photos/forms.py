from django import forms
from .models import Photo, Comment


class PhotoUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*',
            'required': True,
            'id': 'id_image'
        })
    )
    caption = forms.CharField(
        required=False,
        max_length=2200,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none resize-none',
            'placeholder': 'Share your thoughts about this photo...',
            'rows': 4,
            'maxlength': 2200
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'flex-1 px-4 py-2.5 input-dark rounded-xl focus:outline-none',
                'placeholder': 'Add a comment...',
                'maxlength': 500
            })
        }
        labels = {
            'content': ''
        }