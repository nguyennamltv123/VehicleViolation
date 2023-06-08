from django.urls import path
from . import views

urlpatterns = [
    path('',views.list_vehicle, name='veh'),
    # path('', views.List_Vehicle_API.as_view()),
    path('add_vehicle/', views.add_vehicle, name='addvehicle'),
    path('edit_vehicle/<int:pk>/',views.edit_vehicle, name='editvehicle'),
    path('pk=<int:pk>/',views.Detail_Vehicle_API.as_view()),
    path('delete_vehicle/<int:pk>/',views.delete_vehicle, name='deletevehicle'),
    path('add_vehicle_API/',views.Add_Vehicle_API.as_view()),
]
