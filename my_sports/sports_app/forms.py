# In forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Enquiry, Register, Item_entry, KitItem, coachReg, KitPurchase, ItemPurchase, Company, AddRegister, \
    Customer, Coach_Attendence


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'contact_no', 'age']



class CoachAllocation:
    pass


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'mobile', 'email', 'address',   ]

        widgets = {

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last_name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
        }

class CoachForm(forms.ModelForm):
    class Meta:
        model = coachReg
        fields = ['coachname', 'phone', 'email', 'adhar', 'address', 'coachType']

class PurchaseForm(forms.Form):
    item = forms.ModelChoiceField(queryset=KitItem.objects.all())
    quantity = forms.IntegerField(min_value=1, label='Quantity')


class KitPurchaseForm(forms.ModelForm):
    company_name = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label="Select a Company",  # Optional placeholder text
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = KitPurchase
        fields = ['company_name', 'kit_name', 'description', 'quantity', 'price_per_unit']
        widgets = {
            'kit_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
class ItemPurchaseForm(forms.ModelForm):
    class Meta:
        model = ItemPurchase
        fields = ['item_name', 'description', 'company_name','quantity', 'price_per_unit']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['comapny_name', 'address', 'phone_number', 'email', 'other_details']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone_number', 'email', 'address', 'city']








