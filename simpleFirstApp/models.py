from django.db import models

# Create your models here.
from django.urls import reverse

class Teachers(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    department=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    objects=models.Manager()


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return "ID : "+ str(self.id) +" | "+self.course_name
    

    def get_absolute_url(self):
        return reverse("detail_view", kwargs={"pk": self.id})
    


class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE)
    subject_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    standard=models.CharField(max_length=255)
    hobbies=models.CharField(max_length=255)
    roll_no=models.CharField(max_length=255)
    bio=models.TextField()
    profile_image=models.FileField()
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    objects=models.Manager()

    def get_absolute_url(self):
        return reverse("detail_view2", kwargs={"pk": self.id})
    

class StudentSubjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class MultiStepFormModel(models.Model):
    id=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    twitter=models.CharField(max_length=255)
    facebook=models.CharField(max_length=255)
    gplus=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    objects=models.Manager()

class Products(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    desc=models.TextField()

class ProductImages(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    image=models.FileField(max_length=255)
