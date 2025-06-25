from django import forms
from app1.models import Appointment,Address # Assuming you have a model named Appointment in your models.py

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'age', 'mobileno', 'email', 'service', 'date', 'slot']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'state', 'pincode', 'mobileno']


    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(AppointmentForm, self).__init__(*args, **kwargs)

