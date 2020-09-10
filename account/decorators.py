from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseNotFound

# ONLY ALLOW ANONYMOUS USERS
def unauthenticatedUser(viewFunc):
	def wrapperFunction(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('account:homeView')
		return viewFunc(request, *args, **kwargs)
	return wrapperFunction

# ALLOWED ONLY SELECTED USER GROUPS BASED ON PARAMETER PASSED
def allowedUsers(allowedRoles=tuple()):
	def decorator(viewFunc):
		def wrapperFunction(request, *args, **kwargs):
			if kwargs.get('role'):
				role = kwargs['role']
				if role not in allowedRoles:
					return HttpResponseNotFound('<h1>Page not found</h1>')
				return viewFunc(request, *args, **kwargs)
			else:
				if any([request.user.groups.filter(name=group).exists() for group in allowedRoles]):
					return viewFunc(request, *args, **kwargs)
				return HttpResponseNotFound('<h1>Page not found</h1>')
		return wrapperFunction
	return decorator

