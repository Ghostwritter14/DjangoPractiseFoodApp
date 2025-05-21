from django import forms
from .models import Item, CustomCombo


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'item_name',
            'item_description',
            'item_price',
            'item_image',
            'category',
            'ingredients',
        ]

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'item_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'item_image': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter ingredients, separated by commas'
            }),
        }


class CustomComboForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        help_text="Pick up to 3 items from the menu"
    )

    class Meta:
        model = CustomCombo
        fields = ['name', 'items']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Combo name'
            }),
        }

    def clean_items(self):
        items = self.cleaned_data['items']
        if items.count() > 3:
            raise forms.ValidationError("You can select at most 3 items.")
        return items