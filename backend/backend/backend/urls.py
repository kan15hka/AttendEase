from django.contrib import admin
from django.urls import path,include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('checkin/<str:username>',views.checkin,name="checkin"),
    path('checkout/<str:username>',views.checkout,name="checkout"),
    path('employee/<str:username>',views.get_employee_data,name='employee'),
    path('employees/',views.get_all_employee_data,name='employees')
]
