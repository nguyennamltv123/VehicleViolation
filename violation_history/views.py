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