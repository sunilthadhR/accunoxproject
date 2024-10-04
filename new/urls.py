from django.urls import path

# from .models import Friend_List
from .views import signup, login, appcreation, logout, search, cus, all, insert, update, delete, accept_friend, send
from .views import  reject_request,my_list, pending,remove_friend
urlpatterns = [
    path('signup/',signup),
    path('login/',login),
    path('app/',appcreation),
    path('logout/',logout),
    path('search/',search),
    path('customer/<int:id>/',cus),
    path('customer/all/',all),
    path('insert/',insert),
    path('update/<int:id>',update),
    path('delete/<int:id>',delete),
    path('accept/<int:id>',accept_friend),
    path('send/<int:id>',send),
    path('remove/<int:id>',remove_friend),
    path('reject/<int:id>',reject_request),
    path('my_list/<int:id>',my_list),
    path('pending/<int:id>',pending),
    # path('demo/',demo)
]