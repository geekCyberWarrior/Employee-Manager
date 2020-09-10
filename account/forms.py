from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError

from .models import LeaveApplication

from datetime import date

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30,widget=forms.TextInput(
                                    attrs={
                                        'class' : 'form-control', 'placeholder' : 'Username',
                                             'aria-describedby' : 'username-symbol'
        }))
    password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={
                                            'class' : 'form-control', 'placeholder' : 'Password',
                                                 'aria-describedby' : 'password-symbol'
        }))
    password2 = None
    
    class Meta:
        model = User
        fields = [
            'username',
            'password'
            ]
    def __init__(self,*args, **kwargs):
        self.error_messages['invalid_login'] = 'Invalid Username or Password'
        super().__init__(*args, **kwargs)

class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=80, required=True,
                                    widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                    'class' : 'form-control', 'size' : '20',
                                                        'aria-describedby' : 'first_name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class' : 'form-control'
                                                                            ,
                                                                                'aria-describedby' : 'last_name'}))
    username = forms.CharField(max_length=30, required=True,
                                    widget=forms.TextInput(attrs={'class' : 'form-control'
                                                    ,
                                                            'aria-describedby' : 'username'}))
    password1 = forms.CharField(max_length=30, required=True, label = 'Password',
                                    widget=forms.PasswordInput(attrs={
                                    'class' : 'form-control',
                                            'aria-describedby' : 'password1'}))
    password2 = None
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username',
            'password1'
            ]
    def save(self, *args, **kwargs):
        group = kwargs.pop('group')
        user = super().save(*args, **kwargs)
        user.groups.add(group)
        user.save()
        return user

class LeaveApplicationForm(forms.ModelForm):
    startDate = forms.DateField(widget=forms.DateInput(attrs={
                                    'type': 'date', 'class' : 'form-control'}))
    endDate = forms.DateField(widget=forms.DateInput(attrs={
                                    'type': 'date', 'class' : 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={
                                    'rows':5, 'cols':50, 'class' : 'form-control'}))
    totalLeavesAvailable = forms.IntegerField(label='Total Leaves Available',disabled=True,
                                    widget=forms.NumberInput(attrs={
                                            'class' : 'form-control'}))
    class Meta:
        model = LeaveApplication
        exclude = ['user', 'status', 'appliedDetail', 'approvedDetail']

    def __init__(self, leavesAvailable, *args, **kwargs):
        self.leavesAvailable = leavesAvailable
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)

    # VALIDATE THE DATES PASSED FROM THE FORM
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        startDate = cleaned_data['startDate']
        endDate = cleaned_data['endDate']
        if startDate > endDate or startDate < date.today() or (endDate-startDate).days > self.leavesAvailable:
            raise ValidationError(
                        'Enter Valid Details'
                    )