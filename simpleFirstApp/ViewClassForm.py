from django.shortcuts import render
from django.views import View

from simpleFirstApp.forms import TestForm


class ViewClassForm(View):

    def get(self,request,*args,**kwargs):
        form=TestForm()
        return render(request,"testform.html",{"form":form})

    def post(self,request,*args,**kwargs):
        pass