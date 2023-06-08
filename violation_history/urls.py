from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.get_list_violation, name='violation_list'),
    path('add_violation_history/<int:pk>/', views.add_violation_history, name='add_violation_history'),
    path('get_vehicle_has_violation/',views.search_vehicle_has_violation, name='search_vehicle_has_violation'),
    path('unsure_violation/',views.get_list_unsure_violation, name='unsure_violation_list'),
    path('unsure_violation/<int:pk>/',views.get_detail_unsure_violation, name='detail_unsure_violation_list'),
    path('add_vehicle_violation_API/', views.Add_Violation_History_API.as_view()),
    path('add_violation_type/', views.add_violation_type, name='addtype'),
    path('pay_fee/<int:pk>', views.pay_fee, name='payfee'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('delete_unsure_violation/<int:pk>/', views.delete_unsure_violation, name='delete_unsure_violation'),
    path('delete_violation_history/<int:pk>/', views.delete_violation_history, name='delete_violation_history'),
]
