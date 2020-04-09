from django.db import models

# Create your models here.

class Vehicle(models.Model):
    license_number = models.CharField(max_length=20)
    vehicle_image = models.ImageField(upload_to='pics') 
    location=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()

class CameraDb(models.Model):
    ip_address = models.CharField(max_length=30, primary_key=True)
    location = models.CharField(max_length=70)
    camera_type = models.CharField(max_length=70)

class  New_location_db(models.Model):
    location = models.CharField(max_length=70, primary_key=True)

class  New_camera_type_db(models.Model):
    camera_type = models.CharField(max_length=70, primary_key=True)

class AuthUser_db(models.Model):
    u_name = models.CharField(max_length=70, primary_key=True)
    p_word = models.CharField(max_length=70)
    u_role = models.CharField(max_length=70)

class New_role_db(models.Model):
    role = models.CharField(max_length=70)
    