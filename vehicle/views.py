from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Vehicle
from owner.models import Owner
from .serializers import VehicleSerializer
from rest_framework.response import Response
from rest_framework.views  import APIView
from rest_framework import status
from .forms import VehicleForm, SearchingForm
# Create your views here.
def list_vehicle(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            search = request.POST['search']
            vehicle = Vehicle.objects.all().filter(plate__icontains=str(search))
            dt = {
                "Vehicles": vehicle,
                "form": SearchingForm()
            }
            return render(request, 'vehicle/vehicle.html', dt)
        else:
            dt = {"Vehicles": Vehicle.objects.all().order_by("-id"), "form": SearchingForm()}
            return render(request, 'vehicle/vehicle.html', dt)
    else:
        return redirect('login')
    
class List_Vehicle_API(APIView):

    def get(self, request):
        list_vehicle = Vehicle.objects.all()
        dt = VehicleSerializer(list_vehicle, many=True)
        return Response(data=dt.data, status=status.HTTP_200_OK)

def detail_vehicle(request, id):
    if request.user.is_authenticated:
        dt = {"Vehicle": Vehicle.objects.get(id=id),
            "Owner": Owner.objects.exclude(id= id)
        }
        return render(request, 'vehicle/detail_vehicle.html', dt)
    else:
        return redirect('login')
    
class Detail_Vehicle_API(APIView):

    def get(self, request, pk):
        vehicle = Vehicle.objects.get(id=pk)
        dt = VehicleSerializer(vehicle)
        return Response(data=dt.data, status=status.HTTP_200_OK)
    

def add_vehicle(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = VehicleForm(request.POST, request.FILES or None)
            if form.is_valid():
                form.save()
            return redirect('/vehicle')
        elif request.method == "GET":
            context = {'form': VehicleForm()}
            return render(request,"vehicle/add_vehicle.html",context)
    else:
        return redirect('login')


def edit_vehicle(request, pk):
    if request.method == "POST":
        vehicle = Vehicle.objects.get(id=pk)
        form = VehicleForm(request.POST or None, request.FILES or None,instance = vehicle)
        if form.is_valid():
            form.save()
        return redirect('/vehicle')
    elif request.method == "GET":
        vehicle = Vehicle.objects.get(id=pk)
        vehicle_owner = Vehicle.objects.select_related('owner').get(id=pk)
        context = {'form': VehicleForm(instance=vehicle), 'owner': vehicle_owner}
        return render(request,"vehicle/detail_vehicle.html",context)

def delete_vehicle(request, pk):
    if request.user.is_authenticated:
        vehicle = Vehicle.objects.get(id=pk)
        vehicle.delete()
        return redirect("/vehicle")
    else:
        return redirect('login')

class Add_Vehicle_API(APIView):
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def error_404(request, exception):
    return render(request, 'pages/error.html')

def error_500(request):
    return render(request, 'pages/error.html')
