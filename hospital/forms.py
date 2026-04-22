from django import forms
from .models import Patient

PROBLEM_CHOICES = [
    ('Chest Pain', 'Chest Pain'),
    ('Breathing Problem', 'Breathing Problem'),
    ('Fever', 'Fever'),
    ('Headache', 'Headache'),
    ('Accident', 'Accident'),
    ('Bleeding', 'Bleeding'),
    ('Unconscious', 'Unconscious'),
    ('Weakness', 'Weakness'),
]

class PatientForm(forms.ModelForm):
    problems = forms.MultipleChoiceField(
        choices=PROBLEM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    other_problem = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter any additional problem'})
    )

    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'problems', 'other_problem', 'is_emergency']

    def clean(self):
        cleaned_data = super().clean()
        problems = cleaned_data.get('problems')
        other_problem = cleaned_data.get('other_problem')

        if not problems and not other_problem:
            raise forms.ValidationError("Please select at least one symptom or enter another problem.")

        return cleaned_data