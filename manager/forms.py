
from django import forms
from .models import SchoolClass, Subject, Student, Test


class LoginForm(forms.Form):
    username = forms.CharField(label="Admin username")
    pin = forms.CharField(
        label="PIN / Password",
        widget=forms.PasswordInput
    )


class ClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["name"]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name"]


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["school_class", "name", "roll_number"]


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = [
            "school_class",
            "subject",
            "name",
            "test_date",
            "total_marks"
        ]
        widgets = {
            "test_date": forms.DateInput(
                attrs={"type": "date"}
            )
  }
  
