from django import forms

class SearchForm(forms.Form):
    image = forms.ImageField()
