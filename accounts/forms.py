from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
            'placeholder': 'Choose a username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
            'placeholder': 'your.email@example.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none cursor-pointer',
        'accept': 'image/*'
    }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'website']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
                'placeholder': 'your.email@example.com'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none resize-none',
                'placeholder': 'Share your story, interests, or what inspires you...',
                'rows': 5
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 input-dark rounded-xl focus:outline-none',
                'placeholder': 'https://yourwebsite.com'
            }),
        }