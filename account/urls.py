from django.conf.urls import url
from django.urls import path

app_name = 'account'
# from . import views
from . import views
urlpatterns = [
	path('' ,views.homeView, name='homeView'),
    path('login/' ,views.loginView, name='loginView'),
    path('logout/' ,views.logoutRequest, name='logoutRequest'),
    path('signup/<str:role>' ,views.signupView, name='signupView'),
    path('leave/' ,views.leaveView, name='leaveView'),
    path('approve/' ,views.approveView.as_view(), name='approveView'),
    path('approve/<int:id>' ,views.approveApplication, name='approveApplication'),
    path('reject/<int:id>' ,views.rejectApplication, name='rejectApplication'),
	path('view/' ,views.viewView.as_view(), name='viewView'),
]