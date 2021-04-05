from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from simpleFirstApp.models import Subjects, Students


@csrf_exempt
def getSubjects(request):
    subject=Subjects.objects.filter(course_id=request.POST.get('course_id',''))
    subject_obj=serializers.serialize('python',subject)
    return JsonResponse(subject_obj,safe=False)

@csrf_exempt
def savestudent(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    student=Students.objects.get(id=id)
    if type=="name":
       student.name=value

    if type == "email":
        student.email = value

    if type == "standard":
        student.standard = value

    if type == "name":
        student.name = value

    if type == "hobbies":
        student.hobbies = value

    if type == "bio":
        student.bio = value

    if type == "roll_no":
        student.roll_no = value

    if type == "created_at":
        student.created_at = value

    student.save()
    return JsonResponse({"success":"Updated"})


