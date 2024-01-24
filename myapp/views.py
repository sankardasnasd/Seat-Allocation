import base64
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import *


def logout(request):
    request.session['lid']=''
    return HttpResponse(
        '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')


def otp_page(request):
    return render(request,'Otp page.html')

def forget_password(request):
    return render(request,'forget password.html')



def forget_password_post(request):
    em = request.POST['em_add']
    import random
    import string

    # password = random.randint(000000, 999999)


    log = Login.objects.filter(username=em)



    length = 10 # Adjust the password length as needed

    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))



    if log.exists():
        logg = Login.objects.get(username=em)
        message = 'temporary Password  is!... ' + str(password)


        send_mail(
            'temporary...! Password',
            message,
            settings.EMAIL_HOST_USER,
            [em, ],
            fail_silently=False
        )
        logg.password = password
        logg.save()
        return HttpResponse('<script>alert("..Please check Email...");window.location="/myapp/login/"</script>')
    else:
        return HttpResponse('<script>alert("invalid");window.location="/myapp/forget_password/"</script>')




def login(request):
    return render(request,'loginindex.html')


def login_post(request):
    a=request.POST['textfield']
    b=request.POST['textfield2']
    result=Login.objects.filter(username=a,password=b)
    if result.exists():
        result2=Login.objects.get(username=a,password=b)
        request.session['lid']=result2.id
        if result2.type=='admin':
            return HttpResponse('''<script>alert('Admin login success fully');window.location='/myapp/admin_home/'</script>''')


        elif result2.type=='college':
            return HttpResponse('''<script>alert(' login success fully');window.location='/myapp/college_home/'</script>''')


        else:
            return HttpResponse(
                '''<script>alert('invalid');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse(
            '''<script>alert('invalid');window.location='/myapp/login/'</script>''')




def admin_home(request):
    if  request.session['lid']=='':
        return HttpResponse(
        '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')


    return render(request,'admin/adminindex.html')

def add_school(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    return render(request,'admin/add school.html')

def add_school_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    image =request.FILES['image']
    name =request.POST['name']
    place =request.POST['place']
    post =request.POST['post']
    district =request.POST['district']
    phone =request.POST['phone']
    email =request.POST['email']
    type =request.POST['type']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y-%m-%d')+'.jpg'

    fs.save(date,image)
    path=fs.url(date)


    lo=Login()
    lo.username=email
    lo.password=phone
    lo.type='college'
    lo.save()

    sc=College()
    sc.LOGIN=lo
    sc.image=path
    sc.place=place
    sc.name=name
    sc.post=post
    sc.district=district
    sc.phone=phone
    sc.email=email
    sc.type=type
    sc.save()
    return HttpResponse(
        '''<script>alert('Added');window.location='/myapp/admin_home/'</script>''')



def view_college(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=College.objects.all()
    return render(request,'admin/view_collegs.html',{'data':var})

def view_college_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search =request.POST['search']

    var=College.objects.filter(name__icontains=search)

    return render(request,'admin/view_collegs.html',{'data':var})




def delete_college(request,id):
    var=College.objects.get(id=id)
    var.delete()
    return HttpResponse(
        '''<script>alert('success deleted');window.location='/myapp/view_college/'</script>''')



def edit_college(request,id):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=College.objects.get(id=id)

    return render(request,'admin/edit_college.html',{'data':var})

def edit_college_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    id =request.POST['id']
    name = request.POST['name']
    place = request.POST['place']
    post = request.POST['post']
    district = request.POST['district']
    phone = request.POST['phone']
    email = request.POST['email']
    type = request.POST['type']






    sc=College.objects.get(id=id)
    sc.LOGIN=Login.objects.get(id=request.session['lid'])


    if 'image' in request.FILES:
        image = request.FILES['image']

        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'

        fs.save(date, image)
        path = fs.url(date)

        sc.image=path
    sc.place=place
    sc.name=name
    sc.post=post
    sc.district=district
    sc.phone=phone
    sc.email=email
    sc.type=type
    sc.save()
    return HttpResponse(
        '''<script>alert('updated');window.location='/myapp/view_college/'</script>''')



def admin_change_password(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'admin/Admin_change_password.html')



def admin_change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/admin_home/'</script>''')




def view_students(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Student.objects.all()
    return render(request,'admin/view_STUDENTS.html',{'data':var})

def view_students_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    studs=request.POST['search']
    var=Student.objects.filter(name__icontains=studs)
    return render(request,'admin/view_STUDENTS.html',{'data':var})



def view_fecility(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Facilities.objects.all()
    return render(request,'admin/view_fecility.html',{'data':var})
def view_fecility_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search=request.POST['search']

    var=Facilities.objects.filter(COLLEGE__name__icontains=search )
    return render(request,'admin/view_fecility.html',{'data':var})



def allotment_notification(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    data=College.objects.all()
    data2=Course.objects.all()

    return render(request,'admin/alotment_notification.html',{'data':data,'data1':data2})

def allotment_notification_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    college=request.POST['college']
    course=request.POST['course']
    qal=request.POST['qualification']
    v=Shedule_Allotment()
    v.qualification=qal
    v.COLLEGE=College.objects.get(id=college)
    v.COURSE=Course.objects.get(id=course)
    v.date=datetime.now().date().today()
    v.save()
    return HttpResponse(
        '''<script>alert('success ');window.location='/myapp/allotment_notification/'</script>''')

def view_allotment(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Shedule_Allotment.objects.all()
    return render(request,'admin/view_allotments.html',{'data':var})

def view_allotment_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search=request.POST['search']
    search1=request.POST['search1']
    var=Shedule_Allotment.objects.filter(date__range=[search,search1])
    return render(request,'admin/view_allotments.html',{'data':var})


def delete_allotment(request,id):
    var=Shedule_Allotment.objects.get(id=id)
    var.delete()
    return HttpResponse(
        '''<script>alert('success deleted');window.location='/myapp/view_allotment/'</script>''')


def view_complaint(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Complaint.objects.all()
    return render(request,'admin/View_complaint.html',{'data':var})

def view_complaint_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search=request.POST['f']
    search1=request.POST['t']
    var=Complaint.objects.filter(date__range=[search,search1])
    return render(request,'admin/View_complaint.html',{'data':var})


def send_reply(request,id):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Complaint.objects.get(id=id)
    return render(request,'admin/complaint_reply.html',{'data':var})



def complaint_reply_post(request):
    # if request.session['lid']=="":
    #     return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login/'</script>''')

    id = request.POST['id']
    com = request.POST['reply']
    var = Complaint.objects.get(id=id)
    var.reply = com
    var.status = 'Replied'
    var.save()
    return HttpResponse('''<script>alert('successfully sent');window.location='/myapp/view_complaint/'</script>''')




def view_college_review(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=College_review.objects.all()
    return render(request,'admin/View_college_review.html',{'data':var})

def view_college_review_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search=request.POST['f']
    search1=request.POST['t']
    var=College_review.objects.filter(date__range=[search,search1])
    return render(request,'admin/View_college_review.html',{'data':var})





# college Module
def college_home(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    return render(request,'college/collegeindex.html')

def view_college_profile(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=College.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'college/view_profile.html',{'data':var})




def college_view_students(request):
    var=Student.objects.filter(COLLEGE__LOGIN__id=request.session['lid'])
    return render(request,'college/college view students.html',{'data':var})



def college_view_students_post(request):
    s=request.POST['search']
    var=Student.objects.filter(COLLEGE__LOGIN__id=request.session['lid'],name__icontains=s)
    return render(request,'college/college view students.html',{'data':var})


def add_fecility(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    return render(request,'college/add fecility.html')




def add_fecility_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    name=request.POST['name']
    image=request.FILES['image']
    date=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.jpg'
    var=FileSystemStorage()
    var.save(date,image)
    path=var.url(date)


    a=Facilities()
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.name=name
    a.image=path
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/add_fecility/'</script>''')




def view_college_fecility(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Facilities.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/collegeview_fecility.html',{'data':var})

def view_college_fecility_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    search=request.POST['search']
    var=Facilities.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],name__icontains=search)
    return render(request,'college/collegeview_fecility.html',{'data':var})




def delete_fecility(request,id):
    var=Facilities.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>alert('deleted ');window.location='/myapp/view_college_fecility/'</script>''')

def edit_fecility(request,id):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Facilities.objects.get(id=id)

    return render(request,'college/edit fecility.html',{'data':var})

def edit_fecility_post(request):
    id=request.POST['id']
    name=request.POST['name']


    a=Facilities.objects.get(id=id)
    if 'image' in request.FILES:
        image = request.FILES['image']

        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        var = FileSystemStorage()
        var.save(date, image)
        path = var.url(date)
        a.image = path

    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.name=name
    a.save()
    return HttpResponse('''<script>alert('Updated ');window.location='/myapp/view_college_fecility/'</script>''')



def add_depart(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    return render(request,'college/add dept.html')




def add_depart_post(request):
    name=request.POST['name']



    a=Department()
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.name=name
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/add_depart/'</script>''')




def view_college_department(request):
    var=Department.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/collegeview_dept.html',{'data':var})

def view_college_department_post(request):
    search=request.POST['search']
    var=Department.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],name__icontains=search)
    return render(request,'college/collegeview_dept.html',{'data':var})



def delete_dept(request,id):
    var=Department.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>alert('deleted ');window.location='/myapp/view_college_department/'</script>''')




def edit_dept(request,id):
    var=Department.objects.get(id=id)

    return render(request,'college/edit dept.html',{'data':var})

def edit_depart_post(request):
    id=request.POST['id']
    name=request.POST['name']



    a=Department.objects.get(id=id)
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.name=name
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/view_college_department/'</script>''')


def add_course(request,):
    var=Department.objects.all()
    return render(request, 'college/add course.html', {'data': var})


def add_course_post(request):
    # id=request.POST['id']
    name=request.POST['name']
    seats=request.POST['seats']
    de=request.POST['depa']



    a=Course()
    a.name=name
    a.seats=seats
    a.DEPARTMENT=Department.objects.get(id=de)
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/add_course/'</script>''')


def view_college_course(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Course.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/collegeview_course.html',{'data':var})

def view_college_course_post(request):
    search=request.POST['search']
    var=Course.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],name__icontains=search)
    return render(request,'college/collegeview_course.html',{'data':var})

def delete_cour(request,id):
    var=Course.objects.get(id=id)
    var.delete()

    return HttpResponse('''<script>alert('deleted ');window.location='/myapp/view_college_course/'</script>''')



def edit_course(request,id):
    var=Department.objects.all()
    var2=Course.objects.get(id=id)
    return render(request, 'college/edit course.html', {'data1': var,'data':var2})


def edit_course_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    id=request.POST['id']
    name=request.POST['name']
    seats=request.POST['seats']
    de=request.POST['depa']



    a=Course.objects.get(id=id)
    a.name=name
    a.seats=seats
    a.DEPARTMENT=Department.objects.get(id=de)
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert('Updating ');window.location='/myapp/view_college_course/'</script>''')




def add_subject(request,):
    var=Course.objects.all()
    return render(request, 'college/add subject.html', {'data': var})


def add_subject_post(request):
    # id=request.POST['id']
    name=request.POST['name']
    # seats=request.POST['seats']
    de=request.POST['course']



    a=Subject()
    a.name=name
    a.COURSE=Course.objects.get(id=de)
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/add_subject/'</script>''')




def view_college_subject(request):
    var=Subject.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/college_view_subject.html',{'data':var})

def view_college_subject_post(request):
    search=request.POST['search']
    var=Subject.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],name__icontains=search)
    return render(request,'college/college_view_subject.html',{'data':var})


def edit_subject(request,id):
    var=Course.objects.all()
    var2=Subject.objects.get(id=id)
    return render(request, 'college/edit subject.html', {'data1': var,'data':var2})


def edit_subject_post(request):
    id=request.POST['id']
    name=request.POST['name']
    de=request.POST['course']



    a=Subject.objects.get(id=id)
    a.name=name
    a.COURSE=Course.objects.get(id=de)
    a.COLLEGE=College.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert('successfully ');window.location='/myapp/view_college_subject/'</script>''')


def delete_subject(request,id):
    var2=Subject.objects.get(id=id)
    var2.delete()

    return HttpResponse('''<script>alert('deleted ');window.location='/myapp/view_college_subject/'</script>''')



def view_review(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=College_review.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/View_review.html',{'data':var})


def view_review_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    f=request.POST['f']
    t=request.POST['t']
    var=College_review.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],date__range=[f,t])
    return render(request,'college/View_review.html',{'data':var})





def view_sheduled_notification(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Shedule_Allotment.objects.filter(COLLEGE__LOGIN_id=request.session['lid'])
    return render(request,'college/view sheduld allotmet notification.html',{'data':var})

def view_sheduled_notification_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    from1=request.POST['f']
    to=request.POST['t']

    var=Shedule_Allotment.objects.filter(COLLEGE__LOGIN_id=request.session['lid'],date__range=[from1,to])
    return render(request,'college/view sheduld allotmet notification.html',{'data':var})



def view_applied_admission(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='pending')
    return render(request,'college/view admission apply.html',{'data':var})



def view_applied_admission_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    f = request.POST['f']
    t = request.POST['t']

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='pending',date__range=[f,t])
    return render(request,'college/view admission apply.html',{'data':var})



def accept_admission(request,id):


    var=Admission.objects.filter(id=id).update(status='Accept')
    return HttpResponse(
        '''<script>alert('Approved');window.location='/myapp/view_applied_admission/'</script>''')

def reject_admission(request,id):


    var=Admission.objects.filter(id=id).update(status='Reject')
    return HttpResponse(
        '''<script>alert('Rejected');window.location='/myapp/view_applied_admission/'</script>''')




def view_accept_applied_admission(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='Accept')
    return render(request,'college/view accept admission apply request.html',{'data':var})



def view_accept_applied_admission_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    f = request.POST['f']
    t = request.POST['t']

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='Accept',date__range=[f,t])
    return render(request,'college/view accept admission apply request.html',{'data':var})




def view_reject_applied_admission(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='Reject')
    return render(request,'college/view reject admission apply request.html',{'data':var})



def view_reject_applied_admission_post(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    f = request.POST['f']
    t = request.POST['t']

    var=Admission.objects.filter(ALLOTMENT__COLLEGE__LOGIN_id=request.session['lid'],status='Reject',date__range=[f,t])
    return render(request,'college/view reject admission apply request.html',{'data':var})




def college_change_password(request):
    if request.session['lid'] == '':
        return HttpResponse(
            '''<script>alert('You Are LogOut');window.location='/myapp/login/'</script>''')

    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    return render(request,'college/college_change_password.html')




def college_change_password_post(request):
    if request.session['lid'] == "":
        return HttpResponse('''<script>alert(' Logout SuccessFully');window.location='/myapp/login'</script>''')

    old = request.POST['old_password']
    new = request.POST['new_password']
    confirm = request.POST['con_password']
    result=Login.objects.filter(id=request.session['lid'],password=old)
    if result.exists():
        if new==confirm:
            Login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse('''<script>alert('Successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/myapp/college_change_password/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid');window.location='/myapp/college_change_password/'</script>''')

























def login2(request):
    a = request.POST['uname']
    b = request.POST['psw']
    result = Login.objects.filter(username=a, password=b)
    if result.exists():
        result2 = Login.objects.get(username=a, password=b)
        if result2.type == 'student':
            lid=result2.id
            usr=Student.objects.get(LOGIN_id=lid)
            # return JsonResponse({'status':"ok",'lid':str(lid)})
            # return JsonResponse({'status':"ok",'lid':str(lid),'type':'student','photo':usr.image,'name':usr.name})
            return JsonResponse({'status':"ok",'lid':str(lid),'type':'student'})

        else:
            return JsonResponse({'status': 'not Ok'})
    else:
        return JsonResponse({'status': 'not Ok'})




def student_post_new(request):


    name=request.POST['name']
    email=request.POST['email']
    phone=request.POST['phone']
    place=request.POST['place']
    post=request.POST['post']
    qalification=request.POST['qalification']
    COLLEGE=request.POST['COLLEGE']
    password=request.POST['password']
    conf=request.POST['confirm']


    if password==conf:
        image = request.POST['image']
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

        # open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\user\\' + date1, 'wb').write(fs1)
        open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\\student\\' + date1, 'wb').write(fs1)


        path1 = "/media/student/" + date1

        var = Login()
        var.username = email
        var.password = password


        var.type = 'student'
        var.save()

        result = Student()
        result.LOGIN = var
        result.COLLEGE = College.objects.get(id=COLLEGE)
        result.name = name
        result.email = email
        result.phone = phone
        result.qalification = qalification

        result.post=post
        result.place=place

        result.image=path1
        result.save()
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "Not Ok"})



def student_view_complaints(request):
    var=request.POST['lid']
    # var2=Student.objects.get(LOGIN=var)
    result=Complaint.objects.filter(STUDENT__LOGIN_id=var)
    l =[]
    for i in result:
        l.append({'id':i.id, 'complaint':i.complant,'date':i.date,'reply':i.reply,'status':i.status})
    return JsonResponse({'status': "ok", 'data':l})



def student_complaint_post(request):
    var=request.POST['comp']
    lid=request.POST['lid']
    date=datetime.now().date().today()



    c_obj=Complaint()
    c_obj.complant=var
    c_obj.status='pending'
    c_obj.reply='pending'
    c_obj.date=date
    uid=Student.objects.get(LOGIN_id=lid)
    c_obj.STUDENT=uid
    c_obj.save()

    return JsonResponse({'status': "ok"})



def user_changepassword(request):
    lid = request.POST['lid']
    old = request.POST['old']
    newpass = request.POST['new']
    confirm = request.POST['confirm']

    var = Login.objects.filter(id=lid, password=old)
    if var.exists():
        if newpass == confirm:
            var2 = Login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'Not ok'})
    else:
        return JsonResponse({'status': 'NoT Ok'})




def student_profile_new(request):


    lid=request.POST['lid']
    var=Student.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': "ok",'name':var.name,'email':var.email,
                         'phone':var.phone,
                         'image':var.image,
                         'place':var.place,'post':var.post,'COLLEGE':var.COLLEGE.name,'qalification':var.qalification})




def edit_userprofile(request):

    lid = request.POST['lid']
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    image = request.POST['image']
    place = request.POST['place']
    post = request.POST['post']
    qualification = request.POST['qualification']
    COLLEGE = request.POST['COLLEGE']

    result = Student.objects.get(LOGIN_id=lid)
    result.name = name
    result.qalification = qualification
    result.email = email
    result.phone=phone
    result.place=place
    result.post=post
    result.COLLEGE=College.objects.get(id=COLLEGE)

    if len(image) > 1:
        fs1 = base64.b64decode(image)
        date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\student\\' + date1, 'wb').write(fs1)
        path1 = "/media/student/" + date1
        result.image = path1

    # if len(image) > 1:
    #     fs1 = base64.b64decode(image)
    #     date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    #     open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\\student\\' + date1, 'wb').write(fs1)
    #
    #     # open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\\student\\' + date1, 'wb').write(fs1)
    #     path1 = "/media/user/" + date1
    #     result.image = path1

    result.save()
    return JsonResponse({'status': "ok"})


def student_view_college(request):
    var=College.objects.all()
    l=[]

    for i in var:
        l.append({'id':i.id,'type':i.type,'image':i.image,'name':i.name,'place':i.place,'clid':i.LOGIN.id})
        print(l)
    return JsonResponse({'status': "ok",'data':l})



def student_view_fecility(request):
    cid=request.POST['cid']
    var=Facilities.objects.filter(COLLEGE=cid)



    l=[]
    for i in var:
        l.append({'id':i.id,'COLLEGE':i.COLLEGE.name,'image':i.image,'name':i.name,})
    return JsonResponse({'status': "ok",'data':l})



def student_view_departments(request):
    cid=request.POST['did']

    var=Department.objects.filter(COLLEGE_id=cid)



    l=[]
    for i in var:
        l.append({'id':i.id,'COLLEGE':i.COLLEGE.name,'name':i.name})
    return JsonResponse({'status': "ok",'data':l})




def student_view_course(request):

    cid=request.POST['coid']

    var=Course.objects.filter(DEPARTMENT_id=cid)



    l=[]
    for i in var:
        l.append({'id':i.id,'seats':i.seats,'name':i.name})
    return JsonResponse({'status': "ok",'data':l})





def student_view_allotemts(request):

    # cid=request.POST['coid']

    var=Shedule_Allotment.objects.all()



    l=[]
    print(l)
    for i in var:
        l.append({'id':i.id,'COLLEGE':i.COLLEGE.name,'name':i.COURSE.name,'date':i.date,'qualification':i.qualification})
    return JsonResponse({'status': "ok",'data':l})



def apply_admission(request):
    lid=request.POST['lid']
    aid=request.POST['aid']

    image = request.POST['image']
    fs1 = base64.b64decode(image)
    date1 = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"

    # open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\user\\' + date1, 'wb').write(fs1)
    open(r'C:\Users\GAYATHRI\PycharmProjects\seatAllocation\media\\student\\' + date1, 'wb').write(fs1)

    path1 = "/media/student/" + date1




    var=Admission()
    var.ALLOTMENT=Shedule_Allotment.objects.get(id=aid)
    var.STUDENT=Student.objects.get(LOGIN_id=lid)
    var.date=datetime.now().date().today()
    var.status='pending'
    var.file=path1
    var.save()
    return JsonResponse({'status':'ok'})


def view_admission_page(request):
    lid=request.POST['lid']
    var=Admission.objects.filter(STUDENT__LOGIN_id=lid)
    l=[]




    for i in var:
        l.append({'id':i.id,'ALLOTMENT':i.ALLOTMENT.COLLEGE.name,'course':i.ALLOTMENT.COURSE.name,'date':i.date,'status':i.status,'file':i.file})
    return JsonResponse({'status':'ok','data':l})


#
#
#
def chat1(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Student.objects.get(LOGIN=cid)

    return render(request, "college/Chat.html", {'photo': qry.image, 'name': qry.name, 'toid': cid})

def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    qry = Student.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})

    return JsonResponse({'photo': qry.image, "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})




def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})

    return JsonResponse({"status":"ok",'data':l})







# email esisting
# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User

def check_email_exists(request):
    if request.method == 'GET':
        email = request.GET.get('email', None)

        if email:
            user_exists = College.objects.filter(email=email).exists()
            return JsonResponse({'exists': user_exists})

    return JsonResponse({'error': 'Invalid request'})
