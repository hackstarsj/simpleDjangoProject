from django import forms


class TestForm(forms.Form):
    name=forms.CharField(label="Name")
    email=forms.CharField(label="Email")