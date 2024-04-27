from django import forms

class UploadCVForm(forms.Form):
    cv_file = forms.FileField()
