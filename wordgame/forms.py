# wordgame/forms.py

from django import forms

class GuessWordForm(forms.Form):
    guessed_word = forms.CharField(max_length=5, min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
