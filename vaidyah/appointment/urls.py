from django.conf.urls import url
from . import views

app_name = 'appointment'

urlpatterns = [
	url(r'^$', views.index,name='index'),
	url(r'^(?P<doctor_id>[0-9]+)/$', views.detail,name='detail'),

	url(r'^all/', views.alldoctor,name='alldoctor'),
	url(r'^register/$',views.UserFormView.as_view(),name='register'),

	url(r'^help/', views.help,name='help'),
	url(r'^logout/', views.logoutView,name='Logout'),
	url(r'^login/$', views.userlogin,name='login'),
]