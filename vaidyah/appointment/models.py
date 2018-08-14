from django.db import models
from django.contrib.auth.models import User,Permission
from datetime import datetime
from django.core.validators import MaxValueValidator

# Create your models here.

# class User(models.Model):
# 	firstname = models.CharField(max_length=50)
# 	lastname = models.CharField(max_length=50)
# 	email = models.EmailField()
	# password = models.PasswordField()


class Specialization(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title

class Doctor(models.Model):
	#id = models.AutoField(primary_key=True)
	#user = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	qualification = models.CharField(max_length=250,null=False,blank=False)
	experience = models.IntegerField()
	about = models.CharField(max_length=3000)
	photo = models.ImageField(upload_to='media/doctors/',blank=True,null=True)
	country = models.CharField(max_length=15)
	verify = models.BooleanField(default=False)
	rating = models.IntegerField()
	location = models.CharField(max_length=50)
	fees = models.IntegerField()
	specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE)

	# def get_absolute_url(self):
	# 	return reverse('appointment:detail',kwargs={'pk':self.pk})


	def __str__(self):
		return self.name

class Service(models.Model):
	id = models.AutoField(primary_key=True)
	title = models.CharField(max_length = 15)

	def __str__(self):
		return self.title

class Clinic(models.Model):
	id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	location = models.CharField(max_length=100,blank=False)
	phone = models.CharField(max_length=15)
	photo = models.ImageField(upload_to='media/clinic/',blank=True,null=True)
	name = models.CharField(max_length=100)
	service = models.ForeignKey(Service,on_delete=models.CASCADE,blank=True, null=True)
	specialization = models.ForeignKey(Specialization,on_delete=models.CASCADE)
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
	typeof = models.CharField(max_length=50)
	gps = models.CharField(max_length=1000)

	def __str__(self):
		return self.name+'-'+self.location

class Feedback(models.Model):
	doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	date = models.DateField()
	desc = models.CharField(max_length= 100)

	def __str__(self):
		return str(self.date)+'-'+self.desc

class Booking(models.Model):
	doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	#user = models.ForeignKey(User,on_delete=models.CASCADE)
	email = models.EmailField()
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20,db_index = True)
	typeofservice = models.CharField(max_length=150,null=True,blank=True)
	message = models.TextField()
	slot = models.TimeField()
	#charge = models.IntegerField(blank=True,null=True)

	def __str__(self):
		return str(self.slot)

class EmailContent(models.Model):
    message_content = models.TextField(null=True, blank=True)