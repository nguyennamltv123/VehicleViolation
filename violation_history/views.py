from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import ViolationHistory, UnsureViolationHistory
from vehicle.models import Vehicle
from owner.models import Owner
from .forms import SearchingForm
from rest_framework.views  import APIView
from .serializers import ViolationHistorySerializer, UnsureViolationHistorySerializer
from rest_framework.response import Response
from rest_framework import status
import cv2
import easyocr
import glob
import os
import json
# Create your views here.
def get_list_violation(request):
    if request.method == "POST":
        search = request.POST['search']
        violation = ViolationHistory.objects.all().select_related('vehicle').filter(vehicle__plate__icontains=str(search)).order_by("status")
        return render(request, 'history/violation_history.html', {"form": SearchingForm(), "violation": violation})
        # return redirect('/vehicle')
    else:
        return render(request, 'history/violation_history.html', {"form": SearchingForm()})

class Add_Violation_History_API(APIView):
    def post(self, request):
        serializer = UnsureViolationHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            list_of_files = glob.glob(r'D:\Vehicle_Violation\Vehicle_Violation\media\unsureviolation\*')
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)

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
                                    (x + width, y + height), 
                                    (0, 255, 0), 5)
                    plate = img_rgb[y:y+height, x:x+width]
                    cv2.imwrite("result.jpg", plate)


            reader = easyocr.Reader(['en'], gpu=True)
            result = reader.readtext(r"D:\Vehicle_Violation\Vehicle_Violation\result.jpg")
            try:
                ve = Vehicle.objects.get(plate=result[0][-2])
                des = request.POST['description']
                img = request.FILES['image']
                new_vio = ViolationHistory.objects.create(description=des, image= img, vehicle_id= ve.id)
                new_vio.save()
                unsure_vi = UnsureViolationHistory.objects.all().order_by("-id")[0]
                unsure_vi.delete()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_204_NO_CONTENT)

def pay_fee(request, pk):
    if request.method == "POST":
        violation = ViolationHistory.objects.get(id=pk)
        violation.status = True
        violation.save()
        return redirect(f'/pay_fee/{pk}')

    elif request.method == "GET":
        # violation = ViolationHistory.objects.get(id=pk)
        violation = ViolationHistory.objects.select_related('vehicle').get(id=pk)
        return render(request,"history/detail_violation.html", {"Violation": violation})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, "Error")
            return redirect('login')
    else:
        return render(request, 'pages/login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')