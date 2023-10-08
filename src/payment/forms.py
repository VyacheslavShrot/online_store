from django import forms
from phonenumber_field.formfields import PhoneNumberField

from payment.services.novaposhta import get_branches, get_cities
from payment.services.worldwide_shipping import get_european_countries


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


class OrderWorldwideForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Your name"}))
    surname = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"placeholder": "Your surname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "example@example.com"}))
    phone_number = PhoneNumberField(widget=forms.NumberInput(attrs={"placeholder": "+48123456789"}))
    country = forms.ChoiceField(choices=[], required=False)

    def clean_name(self):
        name = self.cleaned_data["name"].capitalize()
        return name

    def clean_surname(self):
        surname = self.cleaned_data["surname"].capitalize()
        return surname

    def __init__(self, *args, **kwargs):
        super(OrderWorldwideForm, self).__init__(*args, **kwargs)

        european_countries = get_european_countries()
        self.fields["country"].choices = european_countries


class DepartmentWorldwideForm(forms.Form):
    city = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={"placeholder": "Your city"}))
    street = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={"placeholder": "Your street"}))
    delivery_service = forms.ChoiceField(
        choices=[
            ("InPost", "InPost"),
            ("Poczta Polska", "Poczta Polska"),
            ("Other", "Select this if you need a different delivery service and put it in the description")
        ],
        required=True
    )
    description = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(attrs={"placeholder": "Description to order *NOT REQUIRED"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(DepartmentWorldwideForm, self).__init__(*args, **kwargs)
