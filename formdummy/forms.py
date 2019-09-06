from django import forms 

class DummyForm(forms.Form):
    text = forms.CharField(label='Отзыв', min_length=3)
