import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','vaidyah.settings')

import django
django.setup()

import random
from appointment.models import Doctor,Specialization,Clinic,Feedback,Service,Booking, User
from faker import Faker

fakegen = Faker()
special = ['Otorhinolaryngologist','Ayurveda','Homoeopath','Dermatologist','Physician','Gynecologist/obstetrician','Dentist']


def add_special():
	s  = Specialization.objects.get_or_create(title=random.choice(special))[0]
	s.save()
	return s

def getRating():
	star = ['1','2','3','4','5']
	return random.choice(star)[0]

def getFees(N):
	return random.choice(range(500,N+1,500))



def populate(N=10):
	for entry in range(N):
		# get the entry for specialization #
		spec = add_special()

		# create fake data#
		fake_spec = fakegen.job()
		fake_name = fakegen.name()
		fake_company = fakegen.company()
		fake_loc = fakegen.street_name()
		fake_fees = getFees(5000)
		fake_qual = fakegen.word()
		fake_exp = fakegen.month()
		fake_about = fakegen.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
		fake_country = fakegen.country()
		fake_veri = fakegen.boolean()
		fake_rating = getRating()
		fake_ph = fakegen.phone_number()
		fake_date = fakegen.date(pattern="%Y-%m-%d", end_datetime=None)
		fake_time = fakegen.time(pattern="%H:%M:%S", end_datetime=None)
		fake_gps = fakegen.geo_coordinate(center=None, radius=0.001)
		fake_desc = fakegen.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
		fake_fname = fakegen.first_name()
		fake_lname = fakegen.last_name()
		fake_email = fakegen.email()

		# create specialization entry
		service = Service.objects.get_or_create(title = fake_spec)
		print(service)

		#create doctor entry
		doctor = Doctor.objects.get_or_create(name=fake_name,qualification=fake_qual,
				experience=fake_exp,about=fake_about,country=fake_country,verify=fake_veri,
				rating=fake_rating,fees = fake_fees,specialization=spec,location=fake_loc)[0]

		print(doctor)
		clinic = Clinic.objects.get_or_create(location=fake_loc,phone=fake_ph,name=fake_company,
				doctor=doctor,specialization=spec,rating=fake_rating,gps=fake_gps)[0]

		feedback = Feedback.objects.get_or_create(doctor=doctor,date=fake_date,desc = fake_desc)[0]


		#user = User.objects.get_or_create(firstname=fake_fname,lastname=fake_lname,email=fake_email)


		book = Booking.objects.get_or_create(doctor=doctor,slot=fake_time)[0]



if __name__=='__main__':
	print('Populating scripts')
	populate(15)
	print('Populating complete')



