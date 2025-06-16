from django import forms
from .models import Teacher

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['bio', 'qualifications', 'documents', 'years_of_experience']
from .models import Teacher

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['bio', 'qualifications', 'documents', 'years_of_experience']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'documents': forms.FileInput(attrs={'class': 'form-control-file'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'})
        }