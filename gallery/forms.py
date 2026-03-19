from django import forms
from .models import Section, MediaItem


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'description', 'order', 'cover_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/webp,video/mp4,video/quicktime'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class MediaUploadForm(forms.Form):
    files = MultipleFileField()
    caption = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional caption for all files'})
    )


class MediaEditForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['caption', 'section']
        widgets = {
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }


class MediaItemBulkUploadForm(forms.ModelForm):
    files = MultipleFileField(required=True)

    class Meta:
        model = MediaItem
        fields = ['section', 'media_type', 'caption', 'files']
