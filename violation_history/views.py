from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import ViolationHistory, UnsureViolationHistory, Violation
from vehicle.models import Vehicle
from owner.models import Owner
from .forms import SearchingForm, ViolationForm
from rest_framework.views  import APIView
from .serializers import ViolationHistorySerializer, UnsureViolationHistorySerializer
from rest_framework.response import Response
from rest_framework import status
import cv2
import easyocr
import glob
import os
# import json
import time
import requests
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def add_violation_type(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ViolationForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('/')
        elif request.method == "GET":
            form = ViolationForm()
            return render(request, 'history/add_violation_type.html', {'form': form})
    else:
        return redirect('login')

@csrf_exempt
def add_violation_history(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            vehicle = Vehicle.objects.get(id=pk)
            violationtype = request.POST['violation_type']
            time = request.POST['time']
            img = request.FILES['image'] or None
            new_vio = ViolationHistory.objects.create(image= img, vehicle_id= pk, violation_id= violationtype, time= time)
            new_vio.save()
            messages.success(request, 'Added violation history!')
            return redirect('/get_vehicle_has_violation')
        elif request.method == "GET":
            vehicle = Vehicle.objects.get(id=pk)
            violation_type = Violation.objects.all()
            dt = {
                'vehicle': vehicle,
                'violation_type': violation_type
            }
            return render(request, 'history/form_add_violation_history.html', dt)
    else:
        return redirect('login')

@csrf_exempt
def search_vehicle_has_violation(request):
    if request.method == "POST":
        search = request.POST['search']
        vehicle = Vehicle.objects.all().filter(plate__icontains=str(search))
        dt = {
                "Vehicles": vehicle,
                "form": SearchingForm()
            }
        return render(request, 'history/add_violation_history.html', dt)
    else:
        dt = {"Vehicles": Vehicle.objects.all().order_by("-id"), "form": SearchingForm()}
        return render(request, 'history/add_violation_history.html', dt)

@csrf_exempt
def get_list_violation(request):
    if request.method == "POST":
        search = request.POST['search']
        # violation = ViolationHistory.objects.all().select_related('vehicle').filter(vehicle__plate__icontains=str(search)).order_by("-id")
        violation = ViolationHistory.objects.all().select_related('vehicle').select_related('violation').filter(vehicle__plate__icontains=str(search)).order_by("-id")
        vi_type = Violation.objects.all().order_by('description')
        return render(request, 'history/violation_history.html', {"form": SearchingForm(), "violation": violation, "vi_type": vi_type})
        # return redirect('/vehicle')
    else:
        vi_type = Violation.objects.all().order_by("description")
        return render(request, 'history/violation_history.html', {"form": SearchingForm(), "vi_type": vi_type})


def get_list_unsure_violation(request):
    if request.user.is_authenticated:
        dt = {
            "violation": UnsureViolationHistory.objects.all().order_by("-id")
        }
        return render(request, 'history/unsure_violation_history.html', dt)
    else:
        return redirect('login')

@csrf_exempt    
def get_detail_unsure_violation(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            confirm = request.POST["confirm"]
            try:
                vehicle = Vehicle.objects.get(plate=str(confirm))
                unsure_vio = UnsureViolationHistory.objects.get(id=pk)
                violation = ViolationHistory.objects.create(description= unsure_vio.description, image= unsure_vio.image, vehicle_id= vehicle.id)
                violation.save()
                unsure_vio.delete()
                messages.success(request, 'Number plate is existed.')
                return redirect(f'/')
            except:
                messages.error(request, 'Cannot find a matched number plate!')
                return redirect(f'/unsure_violation/{pk}')
        else:
            dt = {
                "Violation": UnsureViolationHistory.objects.get(id=pk)
            }
            return render(request, 'history/detail_unsure_violation.html', dt)
    else:
        return redirect('login')

class Get_Vehicle_API(APIView):
    def get(self, request, pla):
        try:
            vehicle = Vehicle.objects.get(plate=pla)
            return Response(status=status.HTTP_200_OK, data={"vehicle_id": vehicle.id})
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

class Add_Unsure_Violation_API(APIView):
    def post(self, request):
        serializer = UnsureViolationHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Add_Violation_API(APIView):
    def post(self, request):
        serializer = ViolationHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Add_Violation_History_API(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UnsureViolationHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_of_files = glob.glob(r'D:\Vehicle_Violation\Vehicle_Violation\media\unsureviolation\*')
            latest_file = max(list_of_files, key=os.path.getctime)

            harcascade = r"D:\Vehicle_Violation\Vehicle_Violation\violation_history\haarcascade_russian_plate_number.xml"
            # Opening image
            img = cv2.imread(latest_file)

            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plate_cascade = cv2.CascadeClassifier(harcascade)

            found = plate_cascade.detectMultiScale(img_gray, 
                                            minSize =(20, 20))

            amount_found = len(found)
            plate = None
            if amount_found != 0:
                for (x, y, width, height) in found:
                    cv2.rectangle(img_rgb, (x, y), 
                                    (x + width + 40, y + height), 
                                    (0, 255, 0), 5)
                    plate = img_rgb[y:y+height, x:x+width+40]
                    cv2.imwrite("plate.jpg", plate)
            if plate is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            try:
                reader = easyocr.Reader(['en'], gpu=True)
                result = reader.readtext(r"D:\Vehicle_Violation\Vehicle_Violation\plate.jpg")
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)
            try:
                os.remove(r"D:\Vehicle_Violation\Vehicle_Violation\plate.jpg")
                ve = Vehicle.objects.get(plate= str(result[0][-2]).upper().replace(' ', ''))
                image = request.FILES['image']
                wideimage = request.FILES['wide_image']
                # new_vio = ViolationHistory.objects.create(image= image, vehicle_id= ve.id, violation_id= 1)
                new_vio = ViolationHistory.objects.create(image= image, wide_image= wideimage, vehicle_id= ve.id, violation_id= 1)
                new_vio.save()
                unsure_vi = UnsureViolationHistory.objects.all().order_by("-id")[0]
                unsure_vi.delete()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)
@csrf_exempt
def pay_fee(request, pk):
    if request.method == "POST":
        violation = ViolationHistory.objects.get(id=pk)
        violation.status = True
        violation.save()
        messages.success(request, 'Paid the fee.')
        return redirect(f'/pay_fee/{pk}')

    elif request.method == "GET":
        # violation = ViolationHistory.objects.get(id=pk)
        violation = ViolationHistory.objects.all().select_related('vehicle').select_related('violation').get(id=pk)
        return render(request,"history/detail_violation.html", {"Violation": violation})

@csrf_exempt
def delete_violation_history(request, pk):
    if request.user.is_authenticated:
        violation = ViolationHistory.objects.get(id=pk)
        violation.delete()
        messages.success(request, 'Deleted violation history!')
        return redirect("/")
    else:
        return redirect('login')

@csrf_exempt
def delete_unsure_violation(request, pk):
    if request.user.is_authenticated:
        un_vi = UnsureViolationHistory.objects.get(id=pk)
        un_vi.delete()
        return redirect("/unsure_violation")
    else:
        return redirect('login')

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "Wrong username or password!")
            return redirect('login')
    else:
        return render(request, 'pages/login.html')
    
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Register successfully!")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

class PasswordsChangeView(PasswordChangeView):
    from_class = PasswordChangeForm
    success_url = reverse_lazy('change_password_done')

def change_password_done(request):
    return render(request, 'pages/password-changed.html')