from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.decorators import login_required
import operator
from django.views.generic import View
from .form import *
from django.contrib.auth import authenticate, login

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout


# Create your views here.


@login_required(login_url='appointment:login')
def alldoctor(request):
	# user = User.objects.get(pk=request.user_id)
	# print(user)
	template_name = 'appointment/doctor.html'
	doctor_list = Doctor.objects.order_by('name')
	return render(request,template_name,{'doctors':doctor_list})

def index(request):
	template_name = 'appointment/visitor.html'
	return render(request,template_name)

@login_required(login_url='appointment:login')
def detail(request,doctor_id):
	template_name = 'appointment/detail.html'
	doctor = Doctor.objects.get(pk=doctor_id)
	return render(request,template_name,{'doctor':doctor})

class UserFormView(View):
	form_obj = UserForm
	template_name = 'appointment/register.html'

	def get(self,request):
		form = self.form_obj(None)
		return render(request,self.template_name,{'form':form})

	def post(self,request):
		form = self.form_obj(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			#cleaned data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#returning user object if credentials are correct
			user = authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request,user)
					return redirect('appointment:alldoctor')
		return render(request,self.template_name,{'form':form})




# @login_required
# def doctor(request):
# 	doctor = Doctor.objects.get(id=request.id)
# 	template_name= 'appointment/detail.html'
# 	return render(request,template_name,{'doctor':doctor})

# def book(request):
# 	template_name = 'appointment/booking.html'
# 	doctor = Doctor.objects.get(id=request.id)
# 	user_d = User.objects.get(id=request.user)

# 	return render(request,template_name,{'doctor':doctor,'user':user_d})


def help(request):
	return render(request,'appointment/help.html')



# class PortalSearchListView(BlogListView):
#     """
#     Display a Blog List page filtered by the search query.
#     """
#     paginate_by = 10

#     def get_queryset(self):
#         result = super(PortalSearchListView, self).get_queryset()

#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )

#         return result
@login_required(login_url='appointment:login')
def takeAppointment(request,doctor_id):
	template_name = 'appointment/booking.html'
	if request.method == 'POST':
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		slot = request.POST.get('slot')
		typeofservice = request.POST.get('typeofservice')
		dec = request.POST.get('dec')
		doctor = Doctor.objects.get(pk=doctor_id)
		booking_obj = Booking(name=name,email=email,phone=phone,message = dec,
			typeofservice=typeofservice,doctor=doctor,slot=slot)
		booking_obj.save()
		doctor_name = Doctor.objects.get(pk=doctor_id)[0]

		################# Send Email to user email and that of admin mail ###############

		
		emailmessage_obj = EmailContent.objects.all()[:0]
		subject = "Thanks for using Vaidyah"
		email=email
		touser = [email]
		from_email = 'vaidyah.me@gmail.com'
		ctx = {
			'name':name,
			'current_date':(time.strftime("%d/%m/%Y")),
			'emailmessage_obj':emailmessage_obj,
			'service':typeofservice,
			'email':email,
			'phone':phone,
			'message':dec,
			'slot':slot,
			'doctor':doctor_name

		}
		message = get_template('user_contact_email.html').render(Context(ctx))
		sending_message = EmailMessage(subject,message,to=touser,from_email=from_email)
		sending_message.content_subtype = 'html'
		sending_message.send()

		######### to admin mail  ###############

		emailmessage_obj = EmailContent.objects.all()[:1]
		message_admin = get_template('appointment/admin_contactus_email.html').render(Context(ctx))
		sending_message_admin = EmailMessage(subject,message,to=[
			x.email for x in AdminEmail.objects.all()],from_email=from_email)
		sending_message_admin.content_subtype = 'html'
		sending_message_admin.send()

		message = 'Success'

	return render(request,template_name,{'message':message})

@login_required(login_url='appointment:login')
def logoutView(request):
	logout(request)
	return redirect('appointment:index')

# def loginView(request):

def userlogin(request):
	template_name = 'appointment/login.html'
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('appointment:alldoctor')
			else:
				return redirect('appointment:index')
		else:
			error= 'Not Valid credentials'
			return render(request,template_name,{'error':error})
	return render(request,template_name)




