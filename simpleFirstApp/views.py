import json

from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from io import StringIO, BytesIO
from requests import request
from simpleDjangoProject import settings
from simpleDjangoProject.settings import EMAIL_HOST_USER
from .models import Students, Teachers, Courses, StudentSubjects, Subjects, MultiStepFormModel, Products, ProductImages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,View,ListView,DetailView,CreateView,UpdateView

# Create your views here.

def FirstPageController(request):
    return HttpResponse("<h1>My First Django Project Page</h1>")

def IndexPageController(request):
    return HttpResponseRedirect("/homePage")

def HtmlPageController(request):
    return render(request,"htmlpage.html")

def HtmlPageControllerWithData(request):
    data1="This is Data 1 Passing to HTML Page"
    data2="This is Data 2 Passing to HTML Page"
    return render(request,"htmlpage_with_data.html",{'data':data1,'data1':data2})

def PassingDatatoController(request,url_data):
    return HttpResponse("<h2>This is Data Coming Via URL : "+url_data)

@login_required(login_url="/login_user/")
def addData(request):
    courses=Courses.objects.all()
    return render(request,"add_data.html",{'courses':courses})

@login_required(login_url="/login_user/")
def add_student(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        profile_img=fs.save(file.name,file)
        try:
            course=Courses.objects.get(id=request.POST.get('course',''))
            student=Students(name=request.POST.get('name',''),email=request.POST.get('email',''),standard=request.POST.get('standard',''),hobbies=request.POST.get('hobbies',''),roll_no=request.POST.get('roll_no',''),bio=request.POST.get('bio',''),profile_image=profile_img,course=course)
            student.save()


            subject_list=request.POST.getlist('subjects[]')
            for subject in subject_list:
                subj=Subjects.objects.get(id=subject)
                student_subject=StudentSubjects(subject_id=subj,student_id=student)
                student_subject.save()
            messages.success(request,"Added Successfully")
        except Exception as e:
            print(e)
            messages.error(request,"Failed to Add Student")

        return HttpResponseRedirect("/addData")

@login_required(login_url="/login_user/")
def add_teacher(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        try:
            teacher=Teachers(name=request.POST.get('name',''),email=request.POST.get('email',''),department=request.POST.get('department',''))
            teacher.save()
            messages.success(request,"Added Successfully")
        except:
            messages.error(request,"Failed to Add Teacher")

        return HttpResponseRedirect("/addData")

@login_required(login_url="/login_user/")
def show_all_data(request):
    all_teacher=Teachers.objects.all()
    all_student=Students.objects.all()

    return render(request,"show_data.html",{'students':all_student,'teachers':all_teacher})

@login_required(login_url="/login_user/")
def delete_student(request,student_id):
    student=Students.objects.get(id=student_id)
    student.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/show_all_data")

@login_required(login_url="/login_user/")
def update_student(request,student_id):
    student=Students.objects.get(id=student_id)
    if student==None:
        return HttpResponse("Student Not Found")
    else:
        return render(request,"student_edit.html",{'student':student})

@login_required(login_url="/login_user/")
def edit_student(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student=Students.objects.get(id=request.POST.get('id',''))
        if student==None:
            return HttpResponse("<h2>Student Not Found</h2>")
        else:
            if request.FILES.get('profile')!=None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_img = fs.save(file.name, file)
            else:
                profile_img=None

            if profile_img!=None:
                student.profile_image=profile_img

            student.name=request.POST.get('name','')
            student.email=request.POST.get('email','')
            student.standard=request.POST.get('standard','')
            student.hobbies=request.POST.get('hobbies','')
            student.roll_no=request.POST.get('roll_no','')
            student.bio=request.POST.get('bio','')
            student.save()

            messages.success(request,"Updated Successfully")
            return HttpResponseRedirect("update_student/"+str(student.id)+"")


def LoginUser(request):
    #print(settings.SECRET_KEY)
    if request.user==None or request.user =="" or request.user.username=="":
        return render(request,"login_page.html")
    else:
        return HttpResponseRedirect("/homePage")

def RegisterUser(request):
    if request.user==None:
        return render(request,"register_page.html")
    else:
        return HttpResponseRedirect("/homePage")

def SaveUser(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username=request.POST.get('username','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')

        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username,email,password)
            messages.success(request,"User Created Successfully")
            return HttpResponseRedirect('/register_user')
        else:
            messages.error(request,"Email or Username Already Exist")
            return HttpResponseRedirect('/register_user')

def DoLoginUser(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed")
    else:
        username=request.POST.get('username','')
        password=request.POST.get('password','')

        user=authenticate(username=username,password=password)

        if user!=None:
            login(request,user)
            return HttpResponseRedirect('/homePage')
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect('/login_user')

@login_required(login_url="/login_user/")
def HomePage(request):
    return render(request,"home_page.html")

def LogoutUser(request):
    logout(request)
    request.user=None
    return HttpResponseRedirect("/login_user")

def testStudent(request):
    student=Students.objects.all()
    student_obj=serializers.serialize('python',student)
    return JsonResponse(student_obj,safe=False)

def SendPlainEmail(request):
    message=request.POST.get('message','')
    subject=request.POST.get('subject','')
    mail_id=request.POST.get('email','')
    email=EmailMessage(subject,message,EMAIL_HOST_USER,[mail_id])
    email.content_subtype='html'
    email.send()
    return HttpResponse("Sent")

def send_mail_plain_with_stored_file(request):
    message=request.POST.get('message','')
    subject=request.POST.get('subject','')
    mail_id=request.POST.get('email','')
    email=EmailMessage(subject,message,EMAIL_HOST_USER,[mail_id])
    email.content_subtype='html'

    file=open("README.md","r")
    file2=open("manage.py","r")
    email.attach("README.md",file.read(),'text/plain')
    email.attach("manage.py",file2.read(),'text/plain')

    email.send()
    return HttpResponse("Sent")


def send_mail_plain_with_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)

    email.send()
    return HttpResponse("Sent")

def setSession(request):
    request.session['session_data_1']="This is Session 1 Data"
    request.session['session_data_2']="This is Session 2 Data"
    return HttpResponse("Session Set")

def view_session(request):
    if request.session.has_key("session_data_1"):
        session_data_1=request.session['session_data_1']
    else:
        session_data_1="Data is Blank"

    if request.session.has_key("session_data_2"):
        session_data_2=request.session['session_data_2']
    else:
        session_data_2="Data is Blank"

    return render(request,"show_session_data.html",{"session_data_1":session_data_1,"session_data_2":session_data_2})

def del_session(request):
    del request.session['session_data_1']
    del request.session['session_data_2']
    return HttpResponse("Session Deleted")

def getPdfPage(request):
    all_student=Students.objects.all()
    data={'students':all_student}
    template=get_template("pdf_page.html")
    data_p=template.render(data)
    response=BytesIO()

    pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
    if not pdfPage.err:
        return HttpResponse(response.getvalue(),content_type="application/pdf")
    else:
        return HttpResponse("Error Generating PDF")

def ShowChatHome(request):
    return render(request,"chat_home.html")

def ShowChatPage(request,room_name,person_name):
    return render(request,"chat_screen.html",{'room_name':room_name,'person_name':person_name})
    #return HttpResponse("Chat page "+room_name+""+person_name)

def multistepformexample(request):
    return render(request,"multistepformexample.html")

def multistepformexample_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("multistepformexample"))
    else:
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        phone=request.POST.get("phone")
        twitter=request.POST.get("twitter")
        facebook=request.POST.get("facebook")
        gplus=request.POST.get("gplus")
        email=request.POST.get("email")
        password=request.POST.get("pass")
        cpass=request.POST.get("cpass")
        if password!=cpass:
            messages.error(request,"Confirm Password Doesn't Match")
            return HttpResponseRedirect(reverse('multistepformexample'))

        try:
            multistepform=MultiStepFormModel(fname=fname,lname=lname,phone=phone,twitter=twitter,facebook=facebook,gplus=gplus,email=email,password=password)
            multistepform.save()
            messages.success(request,"Data Save Successfully")
            return HttpResponseRedirect(reverse('multistepformexample'))
        except:
            messages.error(request,"Error in Saving Data")
            return HttpResponseRedirect(reverse('multistepformexample'))


def multipleUpload(request):
    return  render(request,"multiple_fileupload.html")


def multipleupload_save(request):
    name=request.POST.get("name")
    desc=request.POST.get("desc")
    images=request.FILES.getlist("file[]")
    print(images)
    product=Products(name=name,desc=desc)
    product.save()

    for img in images:
        fs=FileSystemStorage()
        file_path=fs.save(img.name,img)

        pimage=ProductImages(product_id=product,image=file_path)
        pimage.save()


    return HttpResponse("File Uploaded")

def login_firebase(request):
    return render(request,"login_firebase.html")

@csrf_exempt
def firebase_login_save(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    provider=request.POST.get("provider")
    token=request.POST.get("token")
    firbase_response=loadDatafromFirebaseApi(token)
    firbase_dict=json.loads(firbase_response)
    if "users" in firbase_dict:
        user=firbase_dict["users"]
        if len(user)>0:
            user_one=user[0]
            if "phoneNumber" in user_one:
                if user_one["phoneNumber"]==email:
                    data=proceedToLogin(request,email, username, token, provider)
                    return HttpResponse(data)
                else:
                    return HttpResponse("Invalid Login Request")
            else:
                if email==user_one["email"]:
                    provider1=user_one["providerUserInfo"][0]["providerId"]
                    if user_one["emailVerified"]==1 or user_one["emailVerified"]==True or user_one["emailVerified"]=="True" or provider1=="facebook.com":
                        data=proceedToLogin(request,email,username,token,provider)
                        return HttpResponse(data)
                    else:
                        return HttpResponse("Please Verify Your Email to Get Login")
                else:
                    return HttpResponse("Unknown Email User")
        else:
            return HttpResponse("Invalid Request User Not Found")
    else:
        return HttpResponse("Bad Request")


def loadDatafromFirebaseApi(token):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

    payload = 'key=AIzaSyAadzybe3l6sXaFI3-CdUtQ2Ca0EDy1VVE&idToken='+token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = request("POST", url, headers=headers, data=payload)

    return response.text

def proceedToLogin(request,email,username,token,provider):
    users=User.objects.filter(username=username).exists()

    if users==True:
        user_one=User.objects.get(username=username)
        user_one.backend='django.contrib.auth.backends.ModelBackend'
        login(request,user_one)
        return "login_success"
    else:
        user=User.objects.create_user(username=username,email=email,password=settings.SECRET_KEY)
        user_one=User.objects.get(username=username)
        user_one.backend='django.contrib.auth.backends.ModelBackend'
        login(request,user_one)
        return "login_success"


def ajax_file_upload(request):
    return render(request,"ajax_file_upload.html")

@csrf_exempt
def ajax_file_upload_save(request):
    print(request.POST)
    print(request.FILES)
    file1=request.FILES['file1']
    fs=FileSystemStorage()
    file_1_path=fs.save(file1.name,file1)
    file2=request.FILES['file2']
    file_2_path=fs.save(file2.name,file2)
    print(file_1_path)
    print(file_2_path)
    return HttpResponse("Uploaded")

class TemplateViewExample(TemplateView):
    template_name="template_view_example_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data1"] ="DATA1" 
        context["data2"] ="DATA2" 
        return context

    def get_data(self):
        return "Some Data From Method"
    
class ClassBasedViewExample(View):

    def get(self,request,*args,**kwargs):
        return HttpResponse("GET METHOD")

    def post(self,request,*args,**kwargs):
        return HttpResponse("POST METHOD")

class ListBasedViewExample(ListView):
    model=Subjects

class ListBasedViewExample2(ListView):
    model=Courses

class DetailsBasedViewExample(DetailView):
    model=Courses

class DetailsBasedViewExample2(DetailView):
    model=Students

class CreateViewExample(CreateView):
    model=Courses
    fields="__all__"
    #fields=["field1","field2"]

class UpdateViewExample(UpdateView):
    model=Courses
    fields="__all__"


class CreateViewExample2(CreateView):
    model=Students
    fields="__all__"