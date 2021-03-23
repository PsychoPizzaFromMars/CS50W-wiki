from django import forms


class EntryForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class" : "form-control"}))
    entrytext = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))