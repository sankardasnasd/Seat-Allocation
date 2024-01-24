
from django.urls import path
from django.contrib import admin

from myapp import views

urlpatterns = [
    path('otp_page/',views.otp_page),

    path('forget_password/',views.forget_password),
    path('forget_password_post/',views.forget_password_post),

    path('logout/',views.logout),
    path('login/',views.login),
    path('login_post/',views.login_post),

    path('admin_home/',views.admin_home),

    path('admin_change_password/',views.admin_change_password),
    path('admin_change_password_post/',views.admin_change_password_post),

    path('add_school/',views.add_school),
    path('add_school_post/',views.add_school_post),

    path('view_college/',views.view_college),
    path('view_college_post/',views.view_college_post),

    path('edit_college_post/',views.edit_college_post),
    path('delete_college/<id>',views.delete_college),

    path('edit_college/<id>',views.edit_college),

    path('view_students/',views.view_students),
    path('view_students_post/',views.view_students_post),

    path('view_fecility/',views.view_fecility),
    path('view_fecility_post/',views.view_fecility_post),

    path('allotment_notification/',views.allotment_notification),
    path('allotment_notification_post/',views.allotment_notification_post),

    path('view_allotment/',views.view_allotment),
    path('view_allotment_post/',views.view_allotment_post),

    path('delete_allotment/<id>',views.delete_allotment),



    path('view_complaint/',views.view_complaint),
    path('view_complaint_post/',views.view_complaint_post),

    path('send_reply/<id>',views.send_reply),
    path('complaint_reply_post/',views.complaint_reply_post),

    path('view_college_review/',views.view_college_review),
    path('view_college_review_post/',views.view_college_review_post),






    # college module

    path('college_home/',views.college_home),
    path('view_college_profile/',views.view_college_profile),

    path('add_fecility/',views.add_fecility),
    path('add_fecility_post/',views.add_fecility_post),

    path('view_college_fecility/',views.view_college_fecility),
    path('view_college_fecility_post/',views.view_college_fecility_post),

    path('delete_fecility/<id>',views.delete_fecility),

    path('edit_fecility/<id>',views.edit_fecility),
    path('edit_fecility_post/', views.edit_fecility_post),

    path('add_depart/', views.add_depart),
    path('add_depart_post/', views.add_depart_post),

    path('view_college_department/', views.view_college_department),
    path('view_college_department_post/', views.view_college_department_post),

    path('delete_dept/<id>', views.delete_dept),

    path('edit_dept/<id>', views.edit_dept),
    path('edit_depart_post/', views.edit_depart_post),

    path('add_course/', views.add_course),
    path('add_course_post/', views.add_course_post),

    path('view_college_course/', views.view_college_course),
    path('view_college_course_post/', views.view_college_course_post),
    path('edit_course/<id>', views.edit_course),
    path('edit_course_post/', views.edit_course_post),
    path('delete_cour/<id>', views.delete_cour),

    path('add_subject/', views.add_subject),
    path('add_subject_post/', views.add_subject_post),
    path('view_college_subject/', views.view_college_subject),
    path('view_college_subject_post/', views.view_college_subject_post),
    path('delete_subject/<id>', views.delete_subject),
    path('edit_subject/<id>', views.edit_subject),
    path('edit_subject_post/', views.edit_subject_post),

    path('view_review/', views.view_review),
    path('view_review_post/', views.view_review_post),

    path('view_sheduled_notification/', views.view_sheduled_notification),
    path('view_sheduled_notification_post/', views.view_sheduled_notification_post),

    path('view_applied_admission/', views.view_applied_admission),
    path('view_applied_admission_post/', views.view_applied_admission_post),

    path('view_accept_applied_admission/', views.view_accept_applied_admission),
    path('view_accept_applied_admission_post/', views.view_accept_applied_admission_post),

    path('college_change_password/', views.college_change_password),
    path('college_change_password_post/', views.college_change_password_post),

    path('view_reject_applied_admission/', views.view_reject_applied_admission),
    path('view_reject_applied_admission/', views.view_reject_applied_admission),
    path('view_reject_applied_admission_post/', views.view_reject_applied_admission_post),

    path('college_view_students/', views.college_view_students),
    path('college_view_students_post/', views.college_view_students_post),

    path('accept_admission/<id>', views.accept_admission),
    path('reject_admission/<id>', views.reject_admission),









    # stu
    path('login2/', views.login2),
    path('student_post_new/', views.student_post_new),
    path('student_profile_new/', views.student_profile_new),
    path('student_view_complaints/', views.student_view_complaints),
    path('edit_userprofile/', views.edit_userprofile),
    path('user_complaint_post/', views.student_complaint_post),
    path('user_changepassword/', views.user_changepassword),
    path('student_view_college/', views.student_view_college),
    path('student_view_fecility/', views.student_view_fecility),
    path('student_view_departments/', views.student_view_departments),
    path('student_view_course/', views.student_view_course),
    path('student_view_allotemts/', views.student_view_allotemts),
    path('apply_admission/', views.apply_admission),
    path('view_admission_page/', views.view_admission_page),

    path('chat1/<id>',views.chat1),
    path('chat_view/',views.chat_view),
    path('chat_send/<msg>',views.chat_send),
    path('User_sendchat/',views.User_sendchat),
    path('User_viewchat/',views.User_viewchat),

    path('check_email_exists/', views.check_email_exists, name='check_email_exists'),

]
