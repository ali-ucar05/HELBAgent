from django import forms
 
class InputForm(forms.Form):
    prompt = forms.CharField(max_length=200, label='Ask anything :')