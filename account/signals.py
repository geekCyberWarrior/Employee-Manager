from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile, LeaveApplication

from django.shortcuts import render, redirect, get_object_or_404

# ACTIVATED WHEN A USER REGISTERS AND CREATES A PROFILE
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, *args, **kwargs):
	if not Profile.objects.filter(user=instance).exists() and instance.groups.filter(name='Employee').exists():
		Profile.objects.create(user=instance)

# USED TO UPDATE LEAVES WHEN A USER SUBMITS A LEAVE APPLICATION
@receiver(post_save, sender=LeaveApplication)
def updateLeaves(sender, instance, created, *args, **kwargs):
	if created:
		application = LeaveApplication.objects.latest('appliedDetail')
		days = (application.endDate - application.startDate).days + 1
		profile = get_object_or_404(Profile, user=application.user)
		profile.leavesAvailable -= days
		profile.save()