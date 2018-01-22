from django import forms
from . models import Booking,Doctor
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
	class Meta():
		model = Booking
		fields = '__all__'

class UserForm(forms.ModelForm):
	name = forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta():
		model = User
		fields = ['name','email','username','password']

class DoctorForm(forms.ModelForm):

	class Meta():
		model = Doctor
		fields = '__all__'
















