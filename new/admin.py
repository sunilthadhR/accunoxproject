from django.contrib import admin
from .models import Session, usertable, Device, customer,FriendList,Mapping

# Register your models here.
admin.site.register(Device)
admin.site.register(usertable)
admin.site.register(Session)
admin.site.register(customer)
admin.site.register(FriendList)
admin.site.register(Mapping)
