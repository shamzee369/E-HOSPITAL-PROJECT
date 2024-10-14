from django.shortcuts import render,redirect,HttpResponse
from .models import Doctor,Specialization,CustomUser,Appointment,Page,Patient
from django.http import JsonResponse
import random
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone

context = {
    'current_time': timezone.now(),
}

def USERBASE(request):
    
    return render(request, 'userbase.html',context)



def PATIENTREGISTRATION(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('patreg')
        
        else:
            user = CustomUser(
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               user_type=3,
               profile_pic = pic,
            )
            user.set_password(password)
            user.save()
            
            patient = Patient(
                admin = user,
                mobilenumber = mobno,
                gender = gender,
                address = address,
            )
            patient.save()            
            messages.success(request,'Signup Successfully')
            return redirect('patreg')
    

    return render(request, 'user/patient-reg.html')

def PATIENTHOME(request):
    doctor_count = Doctor.objects.all().count
    specialization_count = Specialization.objects.all().count
    context = {
        'doctor_count':doctor_count,
        'specialization_count':specialization_count,

    } 
    return render(request,'user/userhome.html',context)

def Index(request):
    doctorview = Doctor.objects.all()
    first_page = Page.objects.first()

    context = {'doctorview': doctorview,
    'page':first_page,
    }
    return render(request, 'index.html',context)

def Doctors(request):
    doctorview = Doctor.objects.all()
    first_page = Page.objects.first()

    context = {'dv': doctorview,
    'page':first_page,
    }
    return render(request, 'doctor.html',context)

def Aboutus(request):
   
    first_page = Page.objects.first()

    context = {
    'page':first_page,
    }
    return render(request, 'aboutus.html',context)

def Contactus(request):
   
    first_page = Page.objects.first()

    context = {
    'page':first_page,
    }
    return render(request, 'contactus.html',context)

def get_doctor(request):
    if request.method == 'GET':
        s_id = request.GET.get('s_id')
        doctors = Doctor.objects.filter(specialization_id=s_id)
        
        doctor_options = ''
        for doc in doctors:
            doctor_options += f'<option value="{doc.id}">{doc.admin.first_name}</option>'
        
        return JsonResponse({'doctor_options': doctor_options})

import stripe
from django.conf import settings

def create_appointment(request):
    specialization = Specialization.objects.all()

    if request.method == "POST":
        try:
            appointmentnumber = random.randint(100000000, 999999999)
            spec_id = request.POST.get('spec_id')
            doctor_id = request.POST.get('doctor_id')
            date_of_appointment = request.POST.get('date_of_appointment')
            time_of_appointment = request.POST.get('time_of_appointment')
            additional_msg = request.POST.get('additional_msg')

            doc_instance = Doctor.objects.get(id=doctor_id)
            spec_instance = Specialization.objects.get(id=spec_id)
            patientreg = request.user.id
            patient_instance = Patient.objects.get(admin=patientreg)

            # Validate that the appointment date is in the future
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = timezone.now().date()

            if appointment_date <= today_date:
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('patientappointment')

            # Create an appointment but mark fee_paid as False initially
            appointment = Appointment.objects.create(
                appointmentnumber=appointmentnumber,
                pat_id=patient_instance,
                spec_id=spec_instance,
                doctor_id=doc_instance,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                additional_msg=additional_msg,
                fee_paid=False  # Payment not done yet
            )

            messages.info(request, "Your appointment is pending approval from the doctor.")
            return redirect('patientappointment')

        except Doctor.DoesNotExist:
            messages.error(request, "Selected doctor does not exist.")
        except Specialization.DoesNotExist:
            messages.error(request, "Selected specialization does not exist.")
        except Patient.DoesNotExist:
            messages.error(request, "Patient information could not be retrieved.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('patientappointment')

    context = {
        'specialization': specialization
    }
    return render(request, 'user/appointment.html', context)

from django.urls import reverse

def payment_view(request):
    # Get the appointment ID from the query parameters
    appointment_id = request.GET.get('appointment_id')
    
    try:
        # Fetch the appointment from the database
        appointment = Appointment.objects.get(id=appointment_id)

        # Ensure the appointment is approved before proceeding with the payment
        if appointment.status != 'Approved':
            messages.error(request, "You cannot pay for an unapproved appointment.")
            return redirect('view_appointment_history')  # Redirect to appointment history

        # Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create a Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': 'Appointment Fee'},
                    'unit_amount': int(appointment.doctor_id.fee * 100),  # Convert fee to paise
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('appointment_success')) + f"?session_id={{CHECKOUT_SESSION_ID}}&appointment_id={appointment.id}",
            cancel_url=request.build_absolute_uri(reverse('appointment_cancel')),
        )

        # Redirect to the Stripe checkout page
        return redirect(session.url, code=303)  # Stripe requires a 303 redirect

    except Appointment.DoesNotExist:
        # Handle the case where the appointment doesn't exist
        messages.error(request, "Invalid appointment.")
        return redirect('view_appointment_history')
    
import logging

import logging

logger = logging.getLogger(__name__)
def payment_success_view(request):
    session_id = request.GET.get('session_id')
    appointment_id = request.GET.get('appointment_id')

    try:
        # Fetch the appointment from the database
        appointment = Appointment.objects.get(id=appointment_id)
        logger.info(f"Fetched appointment: {appointment}")

        # Check the payment status through Stripe API
        session = stripe.checkout.Session.retrieve(session_id)
        logger.info(f"Stripe session payment status: {session.payment_status}")

        if session.payment_status == 'paid':
            # Update the appointment to set is_paid to True
            appointment.is_paid = True
            
            # Log the state before saving
            logger.info(f"Setting is_paid=True for appointment ID: {appointment.id}")

            try:
                appointment.save()
                logger.info(f"Appointment {appointment.id} saved successfully with is_paid=True.")
            except Exception as e:
                logger.error(f"Error saving appointment {appointment.id}: {str(e)}")

            messages.success(request, "<strong style='color: green;'>Payment was successful! Your appointment is now confirmed.</strong>")
            
            logger.info(f"Payment successful for appointment ID: {appointment.id}. is_paid set to True.")
        else:
            messages.error(request, "Payment was not successful.")
            logger.error(f"Payment status was not 'paid' for session ID: {session_id}. Actual status: {session.payment_status}")

        # Redirect to the appointment details page
        logger.info(f"Redirecting to view_patient_appointment_details with appointment ID: {appointment.id}")
        return redirect('view_patient_appointment_details', appointment_id=appointment.id)

    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        logger.error(f"Appointment ID {appointment_id} does not exist.")
        return redirect('view_appointment_history')
    except Exception as e:
        messages.error(request, f"Payment error: {str(e)}")
        logger.exception("An error occurred during payment processing.")
        return redirect('view_appointment_history')






    
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def view_patient_appointment_details(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)

        # Ensure the payment_url is correctly set up
        payment_url = reverse('payment_view') + f"?appointment_id={appointment.id}"

        # Pass the appointment and its payment status to the template
        context = {
            'appointment': appointment,
            'payment_url': payment_url,
        }
        return render(request, 'user/appointment-history.html', context)
    
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment does not exist.")
        return redirect('view_appointment_history')

 




def appointment_cancel(request):
    messages.error(request, "Payment was canceled. Please try again.")
    return redirect('patientappointment')




def View_Appointment_History(request):
    pat_reg = request.user
    pat_admin = Patient.objects.get(admin=pat_reg)
    userapptdetails = Appointment.objects.filter(pat_id=pat_admin)
    context = {
        'vah':userapptdetails
    }
    return render(request, 'user/appointment-history.html', context)

def cancel_appointment(request, id):
    try:
        appointment = Appointment.objects.get(id=id, pat_id=request.user.patientreg)
        if appointment.status != 'Approved':
            appointment.status = 'Canceled'
            appointment.save()
            messages.success(request, "Your appointment has been canceled successfully.")
        else:
            messages.error(request, "You cannot cancel this appointment.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
    return redirect('view_appointment_history')

def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)
def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)




