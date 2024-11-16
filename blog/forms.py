from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el título de la tarea'
        })
    )
    content = forms.CharField(
        label='Contenido',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa la tarea aquí'
        })
    )

    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise forms.ValidationError('El título debe tener al menos 3 caracteres.')
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 10:
            raise forms.ValidationError('El contenido debe tener al menos 10 caracteres.')
        return content.strip()

class ArticleSearchForm(forms.Form):
    query = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar tareas...'
        })
    )
    status = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=[
            ('', 'Todos'),
            ('active', 'Activas'),
            ('completed', 'Completadas')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
