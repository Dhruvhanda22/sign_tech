from django.db import models
import datetime
from django.utils import timezone
# Create your models here.
class User_detail(models.Model):
    username = models.CharField(max_length=100, null = False)
    email = models.EmailField(max_length=100, null = False)
    password = models.CharField(max_length=1000, null = False)
    hdo = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.email

class User_profile(models.Model):
    user = models.OneToOneField(User_detail, on_delete=models.CASCADE, blank = True, null = True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField( max_length=100)
    city = models.CharField(max_length=100)
    local_place = models.CharField(max_length=100)
    contact = models.CharField( max_length=15)
    date_of_birth = models.DateField()
    signature = models.ImageField(upload_to='user_signature')

    def __str__(self):
        return self.user

class User_CV(models.Model):
    user = models.ForeignKey(User_detail, on_delete=models.CASCADE, blank = True, null = True)
    profession = models.CharField(max_length=100,null = False)
    education = models.CharField(max_length=300, null = False)
    skills = models.TextField(max_length=200,null = True)
    experience_detail = models.TextField(max_length=100, null = False)
    reference_name = models.CharField(max_length=100,null = True)
    reference_workat = models.CharField(max_length=100,null = True)
    reference_position = models.CharField(max_length=100)
    reference_email = models.CharField(max_length=100,null = True)
    reference_contact = models.CharField(max_length=100,null = True)

    def __str__(self):
        return self.user
# model class for Vacancy_Detail
class Vacancy_Detail(models.Model):
    job_title = models.CharField(max_length=50)
    education = models.CharField(max_length=100, null = False)
    range_of_salary = models.IntegerField(null=True, blank=True)
    plus_services = models.CharField( max_length=200)
    experience_year = models.IntegerField(null=False, blank=False)
    task_and_responsibilities = models.TextField(max_length=200)
    qualification_and_experience = models.TextField(max_length=300)
    expiry_date = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    contract_time = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.job_title

class Apply_job(models.Model):
    user = models.ForeignKey(User_detail, on_delete=models.CASCADE, blank = True, null = True)
    vacancy = models.ForeignKey(Vacancy_Detail, on_delete=models.CASCADE, blank = True, null = True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user

class OTP_token(models.Model):
    email = models.EmailField(max_length=100)
    token = models.CharField(max_length=10)

    def __str__(self):
        return self.email

class Contract_detail(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    position = models.CharField(max_length=150)
    salary = models.CharField(max_length=20)
    contract_time = models.IntegerField(null=True, blank=True, default=0)
    signature_value = models.CharField(max_length=550)
    signature_bool = models.BooleanField(default=False)

    def __str__(self):
        return self.email