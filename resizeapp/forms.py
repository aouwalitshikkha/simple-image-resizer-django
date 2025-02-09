from django import forms

FORMAT_CHOICES = [
    ('jpeg', 'JPG'),
    ('png', 'PNG'),
    ('webp', 'WEBP')
]

class ImageResizeForm(forms.Form):
    width = forms.IntegerField(label='Width (px)', required=False, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.IntegerField(label='Height (px)', required=False, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    maintain_aspect_ratio = forms.BooleanField(label='Maintain Aspect Ratio', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    output_format = forms.ChoiceField(choices=FORMAT_CHOICES, label='Output Format', required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    quality = forms.IntegerField(label='Quality (1-100)', required=True, min_value=1, max_value=100, initial=90, widget=forms.NumberInput(attrs={'class': 'form-control'}))
