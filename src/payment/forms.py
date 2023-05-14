from django import forms
from phonenumber_field.formfields import PhoneNumberField

from payment.services.novaposhta import get_branches, get_cities


class OrderForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    surname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Your surname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "example@example.com"}))
    phone_number = PhoneNumberField(widget=forms.NumberInput(attrs={"placeholder": "+380456789012"}))
    city = forms.ChoiceField(choices=[], required=False)

    def clean_name(self):
        name = self.cleaned_data["name"].capitalize()
        return name

    def clean_surname(self):
        surname = self.cleaned_data["surname"].capitalize()
        return surname

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        city = get_cities()
        self.fields["city"].choices = city


class DepartmentForm(forms.Form):
    department = forms.ChoiceField(choices=[], required=True)
    description = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(attrs={"placeholder": "Description to order *NOT REQUIRED"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        city = kwargs.pop("city", None)
        super(DepartmentForm, self).__init__(*args, **kwargs)

        branches = get_branches(city=city)
        choices = [((branch["Description"]), branch["Description"]) for branch in branches]

        self.fields["department"].choices = choices

        if not choices:
            self.fields["department"].choices = [["...", "No post office found in this locality"]]
