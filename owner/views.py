from django.shortcuts import render, redirect, get_object_or_404
from .models import Owner
from .serializers import OwnerSerializer
from rest_framework.response import Response
from rest_framework.views  import APIView
from rest_framework import status
from .forms import OwnerForm, SearchingForm
# Create your views here.
def get_list_owner(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            search = request.POST['search']
            owner = Owner.objects.all().filter(id_card__icontains=str(search))
            data = { 'Owners':  owner,
                "form": SearchingForm()        
            }
            return render(request, 'owner/owner.html', data)
        else:
            data = { 'Owners':  Owner.objects.all().order_by('-id'),
                "form": SearchingForm()        
            }
            return render(request, 'owner/owner.html', data)
    else:
        return redirect('login')
    
class List_Owner_API(APIView):

    def get(self, request):
        list_owner = Owner.objects.all()
        dt = OwnerSerializer(list_owner, many=True)
        return Response(data=dt.data, status=status.HTTP_200_OK)

class Detail_Owner_API(APIView):

    def get(self, request, pk):
        owner = Owner.objects.get(id=pk)
        dt = OwnerSerializer(owner)
        return Response(data=dt.data, status=status.HTTP_200_OK)

def get_detail_owner(request, pk):
    if request.user.is_authenticated:
        detail_owner = Owner.objects.get(id= pk)
        return render(request, 'owner/detail_owner.html', {'Owner': detail_owner})
    else:
        return redirect('login')
    
def add_owner(request):
    if request.method == "POST":
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/vehicle_owner')
    elif request.method == "GET":
        form = OwnerForm()
        return render(request, 'owner/add_owner.html', {'form': form})
    
def edit_owner(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            owner = Owner.objects.get(id=pk)
            form = OwnerForm(request.POST or None, request.FILES or None,instance = owner)
            if form.is_valid():
                form.save()
            return redirect('/vehicle_owner')
        elif request.method == "GET":
            owner = Owner.objects.get(id=pk)
            context = {'form':OwnerForm(instance=owner)}
            return render(request,"owner/detail_owner.html",context)
    else:
        return redirect('login')

class Add_Owner_API(APIView):
    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)