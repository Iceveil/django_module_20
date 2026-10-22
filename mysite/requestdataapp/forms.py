from  django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField(label='Name', max_length=80)
    age = forms.IntegerField(label='Age', min_value=1, max_value=120)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

def validate_filename(file: InMemoryUploadedFile):
    if file.name and 'virus' in file.name:
        raise ValidationError("В имени не может быть слова 'virus' ")

def validate_filesize(file: InMemoryUploadedFile):
    if file.size > 1048576:
        raise ValidationError("файл должен весить не более 1 мб")

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_filename, validate_filesize])