from itertools import count

from django.contrib.gis.utils import mapping
from django.dispatch import receiver
from django.shortcuts import render,redirect
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from  django.core.cache import cache


from .models import usertable, Session, Device, customer, FriendList, Mapping
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
from django.core.paginator import Paginator
from .forms import custom
import time

def hash_string(input_string):
    encoded_string = input_string.encode()
    sha256_hash = hashlib.sha256(encoded_string)
    return sha256_hash.hexdigest()[:50]




@csrf_exempt
def appcreation(request):
    if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            os = data.get('os')
            version = data.get('version')
            serialnumber = data.get('serialnumber')
            register = Device.objects.create(
                 os=os, 
                 version=version,
                 Serialnumber=serialnumber
                )
            device=Device.objects.filter(version=version).last()
            if register:
                sh = Session.objects.create(client_key=hash_string(os))
                sh.device=device
                sh.save()
                return JsonResponse({"message": "app-created", "status": "200"})
    return JsonResponse({"message":"not registered device"})        
     

@csrf_exempt
def signup(request):
    if request.method=='POST':
            data = json.loads(request.body.decode('utf-8'))
            firstname=data.get('firstname')
            lastname=data.get('lastname')
            mobile=data.get('mobile')
            email=data.get('email')
            password=data.get('password')
            value=usertable.objects.filter(email=email).last()
            if not value:
               register1=usertable.objects.create(
                   firstname=firstname,
                   lastname=lastname,
                   mobile=mobile,
                   password=password,
                   email=email,
               )
               return JsonResponse({"message":"created","status":"200"})
            if value:
              return JsonResponse({"message":"already email registered","status":"400"})
    return JsonResponse({"message":"use Post method bro"})
      
import json
@csrf_exempt       
def login(request):
       if request.method == 'POST':
             data = json.loads(request.body.decode('utf-8'))
             email=data.get('email')
             user=usertable.objects.filter(email=email).last()
             password=data.get('password')
             
             if not user :
                 return JsonResponse({"message":"not an registered email id"})
                 
             if user:
                password_value=user.password   
                if email and password == password_value:
                    sess=Session()
                    sess.user=user
                    sess.save()
                    return JsonResponse({"message":"logined","status":"200"})


                if email and password != password_value:
                     return JsonResponse({"message":"password error","status":"400"})




@csrf_exempt  
def logout(request):
       data = json.loads(request.body.decode('utf-8'))
       email=data.get('email')
       userval=usertable.objects.filter(email=email).last()
       sess=Session.objects.filter(user=userval.id).last()
       if not userval:
          return JsonResponse({"message":"no id","status":"200"})
       if userval and  not sess:
            return JsonResponse({"message":"Session everything is closed  ","status":"200"})
       if userval and sess:
            sess.user=None
            sess.save()
            if userval and sess:
                 return JsonResponse({"message":" some session is still there"})


@csrf_exempt          
def search(request):
      data =json.loads(request.body.decode('utf-8'))
      email=data.get('email')
      uservalue=usertable.objects.filter(email=email).all()
      if not uservalue :
           return JsonResponse({"message":" no user "}) 
      if uservalue:
        #    breakpoint()
           val = []
           for i in uservalue:
                dic = {}
                dic["name"] = i.firstname
                dic["mobile"] = i.mobile
                val.append(dic)
        
        #    breakpoint()
           return JsonResponse(data=val, safe=False)



@csrf_exempt
def cus(request,id):
        if request.method == 'GET':
          uservalue=[customer.objects.filter(id=id).last()]
          if uservalue:
            qs_json = serializers.serialize('json', uservalue)
            return JsonResponse({'data':qs_json},safe=False)
@csrf_exempt          
def all(request) :        
        if request.method == 'GET':
             uservalue=customer.objects.all().values()
             user=list(uservalue)
             paginator = Paginator(user, 5)  
             page_number = request.GET.get('page', 1)
             page_obj = paginator.get_page(page_number) 
             return JsonResponse(list(page_obj), safe=False)
           
        
@csrf_exempt         
def insert(request):
    if request.method =='POST':
        data =json.loads(request.body.decode('utf-8'))
        email=data.get('email')
        value=customer.objects.filter(email=email).exists()

        if value:
            return JsonResponse({"message":"already mail_id exits","status":"200"})
        else:
            form = custom(data)
            # form=Custom(data)
            if form.is_valid():
                register = customer(
                    name=form.cleaned_data['name'],
                    Age=form.cleaned_data['Age'],
                    phonenumber=form.cleaned_data['phonenumber'],
                    email=form.cleaned_data['email'],
                    gender=form.cleaned_data['gender'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    )
                register.save()
                return JsonResponse({"message":"data created","status":"200"})
            else:
                return JsonResponse({"message":form.errors,"status":"400"})
    if request.method != "POST":
        return JsonResponse({"message":"method not allowed","code":405,"status":"FAIL"})


@csrf_exempt         
def update(request, pk):
      if request.method =='PUT':
            data = json.loads(request.body.decode('utf-8'))
            uservalue = customer.objects.filter(id=id).last()
            if not  id:
                  return JsonResponse({"message":" in valid id ","status":"200"})
            if id:
                 for key, value in data.items():
                     setattr(uservalue, key, value)
                     uservalue.save()
 
            return JsonResponse({"message":" updated ","status":"200"})


             
@csrf_exempt                 
def delete(request,pk):
     if request.method =='DELETE':
        ip=customer.objects.filter(id=id).last()
        if not  ip:
            return JsonResponse({"message":" in valid id ","status":"200"})
        ip.delete()
        return JsonResponse({"message":" deleted0 ","status":"200"})

@csrf_exempt
def accept_friend(request,id):
    if request.method=='POST':
        ip = customer.objects.filter(id=id).last()
        data = json.loads(request.body.decode('utf-8'))
        name = data.get("name")
        email = data.get("email")
        value = customer.objects.filter(email=email).exists()
        re=Mapping.objects.filter(map=id,rec=ip.name).all()
        friend_list=FriendList.objects.filter(friend_list=id).all()
        list_email = []
        for i in friend_list:
            list_email.append(i.email)
        if email in list_email:
            return JsonResponse({"status": 200, "message": " you already an friend"})
        if value:
                if email and re :
                    breakpoint()
                    if email in ip.email:
                        breakpoint()
                        return JsonResponse({"status": 200, "message": "already you are friend"})
                    if not email in ip.name:
                        breakpoint()
                        val = FriendList.objects.create(name=name, email=email, friend_list=ip)
                        return JsonResponse({"status": 200, "message": "you are now friend"})
                return JsonResponse({"status": 200, "message": " you never sent an request send an request"})
        return JsonResponse({"status":200,"message":"in_valid user"})


@csrf_exempt
def send(request, id):
    if request.method =='POST':
        ip = customer.objects.filter(id=id).first()
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email")
        value = customer.objects.filter(email=email).exists()
        friend_list =FriendList.objects.filter(friend_list=id).all()
        v=[]
        map=Mapping.objects.filter(map=id).all()
        for i in map:
            v.append(i.sender)
        list_email = []
        for i in friend_list:
            list_email.append(i.email)
        if email in list_email:
            return JsonResponse({"status": 200, "message": " you already an friend"})
        if  value :
            if email in v:
                return JsonResponse({"status": 200, "message": " you already sent an request wait until response"})
            email_cache = cache.get(email)
            old_count=count(email_cache)
            breakpoint()
            if old_count and old_count >=3 :
                cache.delete('old_count')
                return JsonResponse({"message":"You crossed limit. you are not able to send more than 3 request within a minute!"})
            if old_count is None:
                breakpoint()
                old_count=0
                se = Mapping.objects.create(sender=email, rec=ip.name, map=ip)
                cache.set('old_count', old_count, timeout=None)
            breakpoint()
            se = Mapping.objects.create(sender=email, rec=ip.name, map=ip)
            new_count=old_count+1
            cache.set('old_count', new_count, timeout=None)
            return JsonResponse({"status": 200, "message": " you successfully sent an request wait until response"})
        return JsonResponse({"status":200,"message":"no are not an valid user"})


@csrf_exempt
def remove_friend(request,id):
    if request.method=='DELETE':
        ip = FriendList.objects.filter(friend_list=id).all()
        list_email=[]
        for i in ip:
            list_email.append(i.email)
        data=json.loads(request.body.decode('utf-8'))
        email=data.get("email")
        if email in list_email:
            FriendList.objects.filter(email=email).delete()
            return JsonResponse({"message":"deleted successfully"})
        return JsonResponse({"message":"you are not in friend_list"})
@csrf_exempt
def my_list(request,id):
    ip=FriendList.objects.filter(friend_list=id).all()
    if ip:
        qs_json = serializers.serialize('json', ip)
        return JsonResponse({'data': qs_json}, safe=False)
    return JsonResponse({"message":"no friend added"})


@csrf_exempt
def pending(request,id):
    value=customer.objects.filter(id=id).all()
    if value:
        ip = Mapping.objects.filter(map=id).all()
        list_email = []
        for i in ip:
            list_email.append(i.sender)
        print(list_email)
        if not ip:
            return JsonResponse({"message": "no pending request"})
        friend_lis = FriendList.objects.filter(friend_list=id).all()
        friend_list=[]
        for i in friend_lis:
            friend_list.append(i.email)
        for i in list_email:
            if i in friend_list:
                Mapping.objects.filter(map=id).delete()
                return JsonResponse({"message":"no pending request"})
            uservalue = Mapping.objects.filter(map=id).values()
            user = list(uservalue)
            return JsonResponse(list(user), safe=False)
    return  JsonResponse({"message":"in-valid user"})


@csrf_exempt
def reject_request(request,id):
    if request.method=='DELETE':
        ip = customer.objects.filter(id=id).last()
        data = json.loads(request.body.decode('utf-8'))
        email = data.get("email")
        email_value = []
        v= customer.objects.filter(email=email).exists()
        value= Mapping.objects.filter(map=id).all()
        for i in value:
            email_value.append(i.sender)
        if id:
            if v:
                if email in email_value:
                    Mapping.objects.filter(sender=email).delete()
                    return JsonResponse({"message": "removed successfully"})
                return JsonResponse({"message": "no request from this user to you"})
            return JsonResponse({"message": "in valid user"})
        return JsonResponse({"message": "in valid id"})
import time
import threading
def timer(request,pk):
    if request.method=='POST':
        my_thread = threading.Thread(target=timer)
        data= json.loads(request.body.decode('utf-8'))
        email=data.get("email")
        email=customer.objects.filter(email=email).last()
        if email :
            my_thread.start()
        time.sleep(20)
        my_thread.join(20)










