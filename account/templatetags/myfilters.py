from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='group') 
def group(user):
	if user.groups.filter(name='Admin').exists():
		return 'Admin'
	if user.groups.filter(name='Manager').exists():
		return 'Manager'
	if user.groups.filter(name='Employee').exists():
		return 'Employee'

@register.filter(name='start')
def start(counter):
	return int(counter)%3 == 0

@register.filter(name='last')
def last(counter):
	return (int(counter)+1)%3 == 0

@register.filter(name='status')
@stringfilter
def status(value):
	d = {
		'p' : 'Pending',
		'r' : 'Rejected',
		'a' : 'Approved',
	}
	if d.get(value):
		return d[value]
	else:
		return 'Pending'

@register.filter(name='color')
@stringfilter
def status(value):
	d = {
		'p' : 'bg-primary',
		'r' : 'bg-danger',
		'a' : 'bg-success',
	}
	if d.get(value):
		return d[value]
	else:
		return 'text-dark'