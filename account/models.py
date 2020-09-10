from django.db import models

# Create your models here.

from django.contrib.auth.models import User


# USED TO KEEP TRACK OF NUMBER OF LEAVES PER EMPLOYEE (DEFAULT = 10)
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	leavesAvailable = models.IntegerField(default=10)

	def __str__(self):
		return self.user.username + ' ' + str(self.leavesAvailable)

class LeaveApplication(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	startDate = models.DateField()
	endDate = models.DateField()
	description = models.TextField(max_length=255)
	status = models.CharField(max_length=1, default='p')
	appliedDetail = models.DateTimeField(auto_now_add=True, null=True)
	approvedDetail = models.DateTimeField(null=True)

	class Meta:
		ordering = ['startDate']

	def __str__(self):
		return self.user.username + ' ' + self.description
