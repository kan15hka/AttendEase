from django.http import JsonResponse
from datetime import timedelta,datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile, CheckInOut
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from collections import defaultdict
import json

# Authentication
@csrf_exempt
def signup(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            username=data.get("username")
            password=data.get("password")
            name=data.get("name")
            role=data.get("role","Employee")
            phone_number=data.get("phone_number","")
            job_title=data.get("job_title","")
            gender=data.get("gender","O")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"message": "Username already taken"}, status=400)
            
            user=User.objects.create_user(username=username,password=password)
            Profile.objects.create(user=user, name=name, role=role, phone_number=phone_number, job_title=job_title, gender=gender)

            return JsonResponse({"message": "User created successfully"}, status=201)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def signin(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                profile = Profile.objects.get(user=user)

                return JsonResponse({
                    "message": "Login successful",
                    "user":{ 
                        'id': profile.id,
                        "name": profile.name,
                        "username": user.username,
                        "role": profile.role,
                        'phone_number': profile.phone_number,
                        'job_title': profile.job_title,
                        'gender': profile.gender,
                    }
                }, status=200)
            else:
                return JsonResponse({"message": "Invalid credentials"}, status=401)
        except Profile.DoesNotExist:
            return JsonResponse({"message": "Profile not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def signout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=405)

# Employee Check In Out
def checkin(request, username):
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return JsonResponse({"message": "Profile not found"}, status=404)

    # current_date=now().date()- timedelta(days=1)
    # current_date=now().date()+ timedelta(days=1)
    current_date = now().date()
    current_time = now().time()

    today_records = CheckInOut.objects.filter(profile=profile, date=current_date).order_by("-check_in_time")

    if today_records.exists():
        last_record = today_records.first()

        if not last_record.check_out_time:
            return JsonResponse({"message": "Already checked in but not checked out"}, status=400)

    new_checkin = CheckInOut.objects.create(profile=profile, date=current_date, check_in_time=current_time)
    return JsonResponse({"message": "Check-in successful", "check_in_time": new_checkin.check_in_time}, status=200)

def checkout(request, username):
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return JsonResponse({"message": "Profile not found"}, status=404)

    # current_date = now().date()- timedelta(days=1)
    # current_date=now().date()+ timedelta(days=1)
    current_date = now().date()
    current_time = now().time()
    today_records = CheckInOut.objects.filter(profile=profile, date=current_date).order_by("-check_in_time")

    if not today_records.exists():
        return JsonResponse({"message": "You have not yet checked in"}, status=400)

    last_record = today_records.first()

    if last_record.check_out_time:
        return JsonResponse({"message": "Already checked out"}, status=400)

    last_record.check_out_time = current_time
    last_record.save()

    return JsonResponse({"message": "Checkout successful", "check_out_time": last_record.check_out_time}, status=200)

# Get employee data
def get_employee_data(request, username):
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return JsonResponse({"message": "Profile not found"}, status=404)

    check_in_outs = CheckInOut.objects.filter(profile=profile)

    # Group check-in and check-out records by date
    grouped_by_date = defaultdict(list)
    for record in check_in_outs:
        grouped_by_date[str(record.date)].append(record)  # Use the date as a string (e.g., "2025-02-25")

    # Prepare the check_in_outs list with grouped data
    check_in_out_data = []
    for date, records in grouped_by_date.items():
        day_check_in_outs = []
        total_worked_time = timedelta()  # Initialize total worked time for the day

        for record in records:
            # Convert check-in time to datetime
            check_in_datetime = datetime.combine(record.date, record.check_in_time)

            # Handle case where check_out_time might be None
            if record.check_out_time:
                # Only calculate worked time if check_out_time exists
                check_out_datetime = datetime.combine(record.date, record.check_out_time)
                worked_time = check_out_datetime - check_in_datetime
                total_worked_time += worked_time
                day_check_in_outs.append({
                    'id': record.id,
                    'check_in_time': record.check_in_time.strftime("%H:%M:%S.%f"),
                    'check_out_time': record.check_out_time.strftime("%H:%M:%S.%f"),
                    'worked_time': worked_time.total_seconds(),  # Worked time in seconds
                    'date': record.date.strftime("%Y-%m-%d")
                })
            else:
                # Handle case where check_out_time is None (if necessary)
                day_check_in_outs.append({
                    'id': record.id,
                    'check_in_time': record.check_in_time.strftime("%H:%M:%S.%f"),
                    'check_out_time': "N/A",  # Indicate N/A if check_out_time is missing
                    'worked_time': 0,  # Worked time is 0 if no check_out_time
                    'date': record.date.strftime("%Y-%m-%d")
                })

        # Calculate first check-in and last check-out for the day, if they exist
        first_check_in = min(records, key=lambda x: x.check_in_time).check_in_time
        last_check_out = max(
            (record.check_out_time for record in records if record.check_out_time),
            default=None
        )

        if last_check_out:
            last_check_out = last_check_out.strftime("%H:%M:%S.%f")
        else:
            last_check_out = "N/A"  # If no check_out_time exists, set it to "N/A"

        check_in_out_data.append({
            date: {
                'first_check_in': first_check_in.strftime("%H:%M:%S.%f"),
                'last_check_out': last_check_out,
                'total_worked_time': total_worked_time.total_seconds(),  # Sum of worked time in seconds
                'day_check_in_outs': day_check_in_outs
            }
        })

    # Construct the response data
    response_data = {
        'id': profile.id,
        'name': profile.name,
        'role': profile.role,
        'phone_number': profile.phone_number,
        'job_title': profile.job_title,
        'gender': profile.gender,
        'check_in_outs': check_in_out_data
    }

    return JsonResponse(response_data)

# Get all employees data
def get_all_employee_data(request):
    profiles = Profile.objects.exclude(role="Admin").all()

    if not profiles:
        return JsonResponse({"message": "No profiles found"}, status=404)

    all_employee_data = []

    for profile in profiles:
        check_in_outs = CheckInOut.objects.filter(profile=profile)

        # Group check-in and check-out records by date
        grouped_by_date = defaultdict(list)
        for record in check_in_outs:
            grouped_by_date[str(record.date)].append(record)

        # Prepare the check_in_outs list with grouped data
        check_in_out_data = []
        for date, records in grouped_by_date.items():
            day_check_in_outs = []
            total_worked_time = timedelta()

            for record in records:
                check_in_datetime = datetime.combine(record.date, record.check_in_time)

                if record.check_out_time:
                    check_out_datetime = datetime.combine(record.date, record.check_out_time)
                    worked_time = check_out_datetime - check_in_datetime
                    total_worked_time += worked_time

                    day_check_in_outs.append({
                        'id': record.id,
                        'check_in_time': record.check_in_time.strftime("%H:%M:%S.%f"),
                        'check_out_time': record.check_out_time.strftime("%H:%M:%S.%f"),
                        'worked_time': worked_time.total_seconds(),
                        'date': record.date.strftime("%Y-%m-%d")
                    })
                else:
                    day_check_in_outs.append({
                        'id': record.id,
                        'check_in_time': record.check_in_time.strftime("%H:%M:%S.%f"),
                        'check_out_time': "N/A",
                        'worked_time': 0,
                        'date': record.date.strftime("%Y-%m-%d")
                    })

            first_check_in = min(records, key=lambda x: x.check_in_time).check_in_time
            last_check_out = max(
                (record.check_out_time for record in records if record.check_out_time),
                default=None
            )

            last_check_out = last_check_out.strftime("%H:%M:%S.%f") if last_check_out else "N/A"

            check_in_out_data.append({
                date: {
                    'first_check_in': first_check_in.strftime("%H:%M:%S.%f"),
                    'last_check_out': last_check_out,
                    'total_worked_time': total_worked_time.total_seconds(),
                    'day_check_in_outs': day_check_in_outs
                }
            })

        # Construct employee data
        employee_data = {
            'id': profile.id,
            'name': profile.name,
            'role': profile.role,
            'phone_number': profile.phone_number,
            'job_title': profile.job_title,
            'gender': profile.gender,
            'check_in_outs': check_in_out_data
        }

        all_employee_data.append(employee_data)

    return JsonResponse({"employees": all_employee_data}, safe=False)


