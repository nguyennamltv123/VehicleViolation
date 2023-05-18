from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_list_owner, name='own'),
    # path('',views.List_Owner_API.as_view()),
    # path('pk=<int:pk>/', views.get_detail_owner, name= 'owner'),
    # path('pk=<int:pk>/', views.Detail_Owner_API.as_view()),
    path('add_owner/',views.add_owner, name='addowner'),
    path('edit_owner/<int:pk>/', views.edit_owner, name='editowner'),
    path('add_owner_API/',views.Add_Owner_API.as_view()),
]
