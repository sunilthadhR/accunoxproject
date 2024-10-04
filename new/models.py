from django.db import models
from datetime import datetime


# Create your models here.
class Device(models.Model):
    os=models.CharField(max_length=20,blank=True,null=True)
    version=models.CharField(max_length=20,blank=True,null=True)
    Serialnumber=models.CharField(max_length=20,blank=True,null=True)
    create_on=models.DateTimeField(auto_now=True)
    modified_on=models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    
   

class usertable(models.Model):
    firstname=models.CharField(max_length=50,blank=True,null=True)
    lastname=models.CharField(max_length=20,blank=True,null=True)
    mobile=models.BigIntegerField(blank=True,null=True)
    email=models.CharField(max_length=50,blank=True,null=True)
    password=models.CharField(max_length=20)
    create_on=models.DateTimeField(auto_now_add=True)
    modified_on=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.email
    
   
class Session(models.Model):
     device = models.ForeignKey(Device, related_name="session",on_delete=models.CASCADE, null=True)
     client_key = models.CharField(max_length=100, null=True, blank=True)
     user = models.ForeignKey(usertable,related_name="user", on_delete=models.CASCADE, null=True)
     ip_address = models.CharField(max_length=50, null=True, blank=True)
     created_on = models.DateTimeField(auto_now_add=True)


class customer(models.Model):
    name=models.CharField(max_length=20,blank=True,null=True)
    Age=models.IntegerField(blank=True,null=True)
    phonenumber=models.BigIntegerField(blank=True,null=True)
    gender=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=20,blank=True,null=True)
    state=models.CharField(max_length=20,blank=True,null=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    
class FriendList(models.Model):
    friend_list=models.ForeignKey(customer, related_name="friend_list",on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(max_length=20,blank=True,null=True)

    objects = models.Manager()



    def __str__(self):
        return str(self.name)

class Mapping(models.Model):
    map=models.ForeignKey(customer,on_delete=models.CASCADE, null=True)
    sender = models.CharField(max_length=20, default="sender")
    rec=models.CharField(max_length=20, default="receiver")
    objects = models.Manager()


