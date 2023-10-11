from django import forms
from .models import Project, Item


class ProjectForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Project
        fields = ['name', 'description', 'url', 'github']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'input m-2',
                    'placeholder': 'Project Name',
                    'required': 'required'
                }),
            'description': forms.Textarea(attrs={'class': 'textarea m-2', 'placeholder': 'Project Description'}),
            'url': forms.URLInput(attrs={'class': 'input m-2', 'placeholder': 'Project URL'}),
            'github': forms.URLInput(attrs={'class': 'input m-2', 'placeholder': 'Github URL'}),
        }



class ItemForm(forms.ModelForm):
    error_css_class = 'error'

    class Meta:
        model = Item
        fields = ['category', 'file', 'description']
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'input m-2', 'placeholder': 'Item Name'}),
            'category': forms.Select(attrs={'class': 'select m-2'}),
            'file': forms.FileInput(attrs={'class': 'button m-2', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'textarea m-2', 'placeholder': 'Item Description'}),
        }


class ItemEditForm(forms.ModelForm):
    error_css_class = 'error'
    class Meta:
        model = Item
        fields = ['category', 'description']
        widgets = {
            # 'name': forms.TextInput(attrs={'class': 'input m-2', 'placeholder': 'Item Name'}),
            'category': forms.Select(attrs={'class': 'select m-2'}),
            'description': forms.Textarea(attrs={'class': 'textarea m-2', 'placeholder': 'Item Description'}),
        }
