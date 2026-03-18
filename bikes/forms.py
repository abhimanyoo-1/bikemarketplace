from django import forms
from .models import Bike, Inquiry


class MultipleFileInput(forms.FileInput):
    """Custom file input widget that supports multiple file selection."""
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is None:
            attrs = {}
        attrs['multiple'] = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return super().value_from_datadict(data, files, name)


class MultipleImageField(forms.ImageField):
    """Custom ImageField that supports multiple files via MultipleFileInput."""
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if isinstance(data, list):
            # Validate each image in the list
            result = []
            for item in data:
                if item:
                    result.append(super().clean(item, initial))
            return result
        return super().clean(data, initial)


class BikeForm(forms.ModelForm):
    images = MultipleImageField(required=False)

    class Meta:
        model = Bike
        fields = [
            'title', 'brand', 'model', 'year', 'engine_cc', 'price', 'mileage',
            'ownership_number', 'fuel_type', 'condition', 'city', 'state',
            'registration_state', 'insurance_validity', 'service_history',
            'negotiable', 'accident_history', 'modifications', 'warranty_remaining',
            'description', 'video'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'modifications': forms.Textarea(attrs={'rows': 3}),
            'insurance_validity': forms.DateInput(attrs={'type': 'date'}),
        }


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['buyer_name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
