from django import forms


class QuizGenerateForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    subject = forms.ModelChoiceField(queryset=None)
    chapter = forms.CharField(max_length=150)
    use_ai = forms.BooleanField(required=False)

    def __init__(self, *args, subject_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = subject_queryset
