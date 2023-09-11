from django import forms

class ReportForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "example@example.com"}))
    description = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(attrs={"placeholder": "Report description"}),
        required=True,
        min_length=20
    )
