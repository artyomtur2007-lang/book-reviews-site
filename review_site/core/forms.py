from django import forms
from .models import Review
from .models import Book, Genre

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваш отзыв...'
            }),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'year', 'description', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'genres': forms.CheckboxSelectMultiple(),
        }