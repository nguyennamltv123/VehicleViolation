from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.get_list_violation, name='violation_list'),
    path('add_vehicle_violation_API/', views.Add_Violation_History_API.as_view()),
    path('pay_fee/<int:pk>', views.pay_fee, name='payfee'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout')
]
