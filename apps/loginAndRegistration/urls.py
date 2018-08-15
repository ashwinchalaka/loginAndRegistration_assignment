from django.conf.urls import url
from . import views

urlpatterns = [
    url ('^$', views.index, name='home'),
    url ('^processReg$', views.processRegistration, name='processRegistration'),
    url ('^processLogin$', views.processLogin, name='processLogin'),
    url ('^processLogout$', views.processLogout, name='processLogout'),
    url ('^loggedIn$', views.login, name='loggedin'),
]