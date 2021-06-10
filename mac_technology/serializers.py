from rest_framework import serializers
from .models import *

class User_detailSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User_detail
        fields = '__all__'
    
class Profile_detailSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User_profile
        fields = '__all__'

class Vacancy_detailSerilizer():
    class Meta:
        model = Vacancy_Detail
        fields = '__all__'

class CV_detailSerilizer():
    class Meta:
        model = User_CV
        fields = '__all__'

class Apply_job_detailSerilizer():
    class Meta:
        model = Apply_job
        fields = '__all__'