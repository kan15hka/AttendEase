from rest_framework import serializers
from .models import Profile,CheckInOut

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ['id', 'user', 'name', 'role', 'phone_number', 'job_title', 'gender']

class CheckInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model=CheckInOut
        fields = ['id', 'profile', 'check_in_time', 'check_out_time', 'date', 'worked_hours']

