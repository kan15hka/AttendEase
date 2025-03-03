from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    name=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    job_title = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O')

    def __str__(self):
        return f"{self.name} - {self.role}"
    
class CheckInOut(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="check_in_outs")
    check_in_time=models.TimeField()
    check_out_time=models.TimeField(null=True,blank=True)
    date=models.DateField()

    def __str__(self):
        return f"{self.profile.name}: {self.date}: {self.check_in_time} - {self.check_out_time}"
    
