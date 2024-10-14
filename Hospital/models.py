from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'doc'),
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')
    
        # Override the groups and user_permissions fields to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # unique related_name for CustomUser
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # unique related_name for CustomUser
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Specialization(models.Model):
    sname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sname
   
    

class Doctor(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mobilenumber = models.CharField(max_length=11)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False) 

    def __str__(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"
        else:
            return f"User not associated - {self.mobilenumber}"


class Patient(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11,unique=True)
    gender = models.CharField(max_length=100)
    address = models.TextField()
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    appointmentnumber = models.IntegerField(default=0)
    spec_id = models.ForeignKey(Specialization, on_delete=models.CASCADE,default=0)
    pat_id = models.ForeignKey(Patient, on_delete=models.CASCADE,default=0)    
    date_of_appointment = models.CharField(max_length=250)
    time_of_appointment = models.CharField(max_length=250)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    additional_msg = models.TextField(blank=True)
    remark = models.CharField(max_length=250,default=0)
    status = models.CharField(default=0,max_length=200)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fee_paid = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    

class Page(models.Model):
    pagetitle = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    aboutus = models.TextField()
    email = models.EmailField(max_length=200)
    mobilenumber = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pagetitle

class AddPatient(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobilenumber = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=200)
    gender = models.CharField(max_length=100)
    address = models.TextField()
    age = models.IntegerField()
    
    medicalhistory = models.TextField()
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MedicalHistory(models.Model):
    pat_id = models.ForeignKey(AddPatient, on_delete=models.CASCADE, related_name='medical_histories', default=0)
    bloodpressure = models.CharField(max_length=250)
    weight = models.CharField(max_length=250)
    bloodsugar = models.CharField(max_length=250)
    bodytemp = models.CharField(max_length=250)
    prescription = models.TextField()
    visitingdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
prescription_file = models.FileField(upload_to='prescriptions/', null=True, blank=True) 
 
