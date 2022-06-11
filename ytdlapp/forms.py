from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(min_length=3, max_length=500, label=False,
    widget=forms.TextInput(
        attrs={
            'placeholder':'enter-url',
            'class':'form-control',
            'id':'exampleFormControlInput1',
            }))