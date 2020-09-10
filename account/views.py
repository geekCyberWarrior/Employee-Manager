from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound

# Create your views here.
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import LoginForm, SignUpForm, LeaveApplicationForm

from .decorators import unauthenticatedUser, allowedUsers

from .models import Profile, LeaveApplication
from django.views.generic import ListView

from datetime import datetime

@unauthenticatedUser
def loginView(request):
    form = LoginForm(request=request, data=request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('account:homeView')
            else:
                form = LoginForm()
                messages.error(request, 'Invalid username or password')
        else:
            form = LoginForm()
            messages.error(request, 'Invalid username or password')
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)

@login_required
def logoutRequest(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('account:loginView')

@unauthenticatedUser
@allowedUsers(allowedRoles=('admin', 'manager', 'employee'))
def signupView(request, role):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(name=role.title())
            user = form.save(group=group)
            login(request, user)
            return redirect('account:homeView')
        else:
            messages.error(request, 'Username already exists')
            form = SignUpForm()
    else:
        form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'account/signup.html', context)

@login_required
def homeView(request):
    return render(request, 'account/home.html')

@login_required
@allowedUsers(allowedRoles=('Employee',))
def leaveView(request):
    leavesAvailable = Profile.objects.get(user=request.user).leavesAvailable
    form = LeaveApplicationForm(leavesAvailable=leavesAvailable, data=request.POST or None, initial={'totalLeavesAvailable': leavesAvailable})
    if request.method == 'POST':
        form = LeaveApplicationForm(leavesAvailable=leavesAvailable, data=request.POST)
        form.initial['totalLeavesAvailable'] = leavesAvailable
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, 'Application successfully submitted.')
            return redirect('account:homeView')
    context = {
        'form': form
    }
    return render(request, 'account/leave.html', context)

class approveView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    raise_exception = True
    template_name = 'account/approveApplications.html'
    queryset = LeaveApplication.objects.filter(status='p')
    def test_func(self):
        allowedRoles = ('Manager',)
        return all([self.request.user.groups.filter(name=group).exists() for group in allowedRoles])

@login_required
@allowedUsers(allowedRoles=('Manager',))
def approveApplication(request, id):
    if request.method == 'POST':
        application = get_object_or_404(LeaveApplication, id=id)
        application.status = 'a'
        application.approvedDetail = datetime.now()
        application.save()
        messages.info(request, 'Application successfully approved!')
        return redirect('account:homeView')
    return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
@allowedUsers(allowedRoles=('Manager',))
def rejectApplication(request, id):
    if request.method == 'POST':
        application = get_object_or_404(LeaveApplication, id=id)
        application.status = 'r'
        application.approvedDetail = datetime.now()
        application.save()
        messages.info(request, 'Application successfully rejected.')
        return redirect('account:homeView')
    return HttpResponseNotFound('<h1>Page not found</h1>')

# PASS DYNAMIC QUERYSETS BASED ON THE USER GROUP (ADMIN OR EMPLOYEE)
class viewView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    raise_exception = True
    template_name = 'account/view.html'
    def test_func(self):
        allowedRoles = ('Admin', 'Employee')
        return any([self.request.user.groups.filter(name=group).exists() for group in allowedRoles])
    def get_queryset(self):
        if self.request.user.groups.filter(name='Employee').exists():
            return LeaveApplication.objects.filter(user=self.request.user)
        return LeaveApplication.objects.all()