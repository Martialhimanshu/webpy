from django.contrib import admin
from appointment.models import Doctor,Specialization,Clinic,Feedback,Service,Booking
#from appointment.models import User


# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialization)
#admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(Feedback)
admin.site.register(Clinic)