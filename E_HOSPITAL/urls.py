"""
URL configuration for E_HOSPITAL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Hospital import views,patientviews,doctorviews,adminviews

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    

    # path for login,logout,profile update and approval 
    path('', patientviews.Index, name='index'),
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('login/', views.LOGIN, name='login'),
    
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('pending-doctors/', adminviews.view_pending_doctors, name='view_pending_doctors'),
    path('approve-doctor/<int:doctor_id>/', adminviews.approve_doctor, name='approve_doctor'),
    path('reject-doctor/<int:doctor_id>/', adminviews.reject_doctor, name='reject_doctor'),
    path('still-pending/', adminviews.still_pending, name='still_pending'),
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),




    # path for admin access 

    path('Admin/AdminHome', adminviews.ADMINHOME, name='admin_home'),
    path('Admin/Specialization', adminviews.SPECIALIZATION, name='add_specilizations'),
    path('Admin/ManageSpecialization', adminviews.MANAGESPECIALIZATION, name='manage_specilizations'),
    path('Admin/DeleteSpecialization/<str:id>', adminviews.DELETE_SPECIALIZATION, name='delete_specilizations'),
    path('UpdateSpecialization/<str:id>', adminviews.UPDATE_SPECIALIZATION, name='update_specilizations'),
    path('UPDATE_Specialization_DETAILS', adminviews.UPDATE_SPECIALIZATION_DETAILS, name='update_specilizations_details'),
    path('Admin/DoctorList', adminviews.DoctorList, name='viewdoctorlist'),
    path('Admin/ViewDoctorDetails/<str:id>', adminviews.ViewDoctorDetails, name='viewdoctordetails'),
    path('Admin/ViewDoctorAppointmentList/<str:id>', adminviews.ViewDoctorAppointmentList, name='viewdoctorappointmentlist'),
    path('Admin/ViewDOCPatient/<str:id>', adminviews.View_DOCPatient, name='viewdocpatient'),
    path('Admin/ViewCheckPatient/<str:id>', adminviews.ViewCheckAddPatient, name='viewcheckaddpatient'),

   
    path('Admin/ViewPatientDetails/<str:id>', adminviews.ViewPatientDetails, name='viewpatientdetails'),
    path('SearchDoctor', adminviews.Search_Doctor, name='search_doctor'),
    path('Admin/RegUsers', adminviews.RegUsersDetails, name='regusers'),
    path('Admin/DeleteRegusers/<str:id>', adminviews.DELETE_REGUSERS, name='delusersdetails'),
    path('Admin/RegUserAppointment/<str:id>', adminviews.Reg_User_Appoinments, name='regusersapp'),

    path('DoctorBetweenDateReport', adminviews.Doctor_Between_Date_Report, name='doctor_between_date_report'),


    # path for website information change 
     path('Website/update', adminviews.WEBSITE_UPDATE, name='website_update'),
     path('UPDATE_WEBSITE_DETAILS', adminviews.UPDATE_WEBSITE_DETAILS, name='update_website_details'),



    #  path for doctor views
     # This is Doctor Panel
    path('docsignup/', doctorviews.DOCSIGNUP, name='docsignup'),
    path('Doctor/DocHome', doctorviews.DOCTORHOME, name='doctor_home'),
    path('Doctor/AddPatient', doctorviews.Add_Patient, name='add_patient'),
    path('Doctor/ManagePatient', doctorviews.Manage_Patient, name='manage_patient'),
    path('Doctor/ViewPatient/<str:id>', doctorviews.View_Patient, name='viewpatient'),
    path('Doctor/EditPatient', doctorviews.edit_patient, name='editpatient'),
    path('Doctor/ViewCheckPatient/<str:id>', doctorviews.ViewCheckPatient, name='viewcheckpatient'),
    path('Doctor/UpdateMedRecPatient', doctorviews.update_med_rec_patient, name='updatemedrecpatient'),
    path('Doctor/ViewAppointment', doctorviews.View_Appointment, name='view_appointment'),
    path('DoctorPatientAppointmentDetails/<str:id>', doctorviews.Patient_Appointment_Details, name='patientappointmentdetails'),
    path('AppointmentDetailsRemark/Update', doctorviews.Patient_Appointment_Details_Remark, name='patient_appointment_details_remark'),
    path('DoctorPatientApprovedAppointment', doctorviews.Patient_Approved_Appointment, name='patientapprovedappointment'),
    path('DoctorPatientCancelledAppointment', doctorviews.Patient_Cancelled_Appointment, name='patientcancelledappointment'),
    path('DoctorPatientNewAppointment', doctorviews.Patient_New_Appointment, name='patientnewappointment'),
    path('DoctorPatientListApprovedAppointment', doctorviews.Patient_List_Approved_Appointment, name='patientlistappointment'),

    path('DoctorAppointmentList/<str:id>', doctorviews.DoctorAppointmentList, name='doctorappointmentlist'),
    path('PatientAppointmentPrescription', doctorviews.Patient_Appointment_Prescription, name='patientappointmentprescription')
    
    ,
    path('prescription/download/<int:appointment_id>/', doctorviews.download_prescription, name='download_prescription'),

    path('PatientAppointmentCompleted', doctorviews.Patient_Appointment_Completed, name='patientappointmentcompleted'),
    path('SearchAppointment', doctorviews.Search_Appointments, name='search_appointment'),
    path('SearchPatient', doctorviews.Search_Patient, name='search_patient'),
    path('BetweenDateReport', doctorviews.Between_Date_Report, name='between_date_report'),
    path('BetweenDatePatientReport', doctorviews.Between_Date_Patient_Report, name='between_date_patient_report'),



    # path for patient views
        path('PatientRegsitratios', patientviews.PATIENTREGISTRATION, name='patreg'),
    path('Pat/PatHome', patientviews.PATIENTHOME, name='userhome'),
    path('userbase/', patientviews.USERBASE, name='userbase'),
    path('', patientviews.Index, name='index'),
    path('patientappointment/', patientviews.create_appointment, name='patientappointment'),
    path('payment/', patientviews.payment_view, name='payment_view'),
     path('payment/success/', patientviews.payment_success_view, name='appointment_success'),
    path('appointment/cancel/', patientviews.appointment_cancel, name='appointment_cancel'),
     path('ViewAppointmentDetails/<int:appointment_id>/', patientviews.view_patient_appointment_details, name='view_patient_appointment_details'),

    
    path('get_doctor/', patientviews.get_doctor, name='get_doctor'),
    path('User_SearchAppointment', patientviews.User_Search_Appointments, name='user_search_appointment'),
    path('ViewAppointmentHistory', patientviews.View_Appointment_History, name='view_appointment_history'),
    path('cancel_appointment/<str:id>', patientviews.cancel_appointment, name='cancel_appointment'),
    path('ViewAppointmentDetails/<str:id>/', patientviews.View_Appointment_Details, name='viewappointmentdetails'),
    path('Doctor', patientviews.Doctors, name='doctor'),
    path('Aboutus', patientviews.Aboutus, name='aboutus'),
    path('Contactus', patientviews.Contactus, name='contactus'), 
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)