from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)



class College(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    image=models.CharField(max_length=500)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class Facilities(models.Model):
    COLLEGE=models.ForeignKey(College,on_delete=models.CASCADE)
    image=models.CharField(max_length=500)
    name=models.CharField(max_length=100)

class Department(models.Model):
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Course(models.Model):
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seats = models.CharField(max_length=100)

class Subject(models.Model):
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)




class Student(models.Model):
    image=models.CharField(max_length=500)
    name=models.CharField(max_length=100)
    qalification=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)

    # COURSE=models.ForeignKey(Course,on_delete=models.CASCADE)


class College_review(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)
    review = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)


class Complaint(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    complant = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)


class Shedule_Allotment(models.Model):
    COLLEGE = models.ForeignKey(College, on_delete=models.CASCADE)
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)


class Admission(models.Model):
    ALLOTMENT= models.ForeignKey(Shedule_Allotment, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    # name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    file = models.CharField(max_length=500)


class Chat(models.Model):
    FROMID= models.ForeignKey(Login,on_delete=models.CASCADE,related_name="Fromid")
    TOID= models.ForeignKey(Login,on_delete=models.CASCADE,related_name="Toid")
    message=models.CharField(max_length=100)
    date=models.DateField()