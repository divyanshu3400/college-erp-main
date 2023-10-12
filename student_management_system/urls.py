from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from student_management_app import views, HodViews, StaffViews, StudentViews,AccountantView
from student_management_app.EditResultVIewClass import EditResultViewClass
from student_management_system import settings

urlpatterns = [
    path('demo',views.showDemoPage),
    path('signup_admin',views.signup_admin,name="signup_admin"),
    path('signup_student',views.signup_student,name="signup_student"),
    path('signup_staff',views.signup_staff,name="signup_staff"),
    path('signup_accountant',views.signup_accountant,name="signup_accountant"),
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('do_staff_signup',views.do_staff_signup,name="do_staff_signup"),
    path('do_accountant_signup',views.do_accountant_signup,name="do_accountant_signup"),
    path('do_signup_student',views.do_signup_student,name="do_signup_student"),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',HodViews.admin_home,name="admin_home"),
    path('add_staff',HodViews.add_staff,name="add_staff"),
    path('add_staff_save',HodViews.add_staff_save,name="add_staff_save"),
    path('add_accountant',HodViews.add_accountant,name="add_accountant"),
    path('add_accountant_save',HodViews.add_accountant_save,name="add_accountant_save"),
    path('add_course/', HodViews.add_course,name="add_course"),
    path('add_course_save', HodViews.add_course_save,name="add_course_save"),
    path('add_student', HodViews.add_student,name="add_student"),
    path('add_student_save', HodViews.add_student_save,name="add_student_save"),
    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_accountant', HodViews.manage_accountant,name="manage_accountant"),
    path('manage_student', HodViews.manage_student,name="manage_student"),
    path('manage_course', HodViews.manage_course,name="manage_course"),
    path('manage_subject', HodViews.manage_subject,name="manage_subject"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff,name="edit_staff"),
    path('edit_accountant/<str:accountant_id>', HodViews.edit_accountant,name="edit_accountant"),
    path('delete_staff/<str:staff_id>', HodViews.delete_staff,name="delete_staff"),
    path('edit_staff_save', HodViews.edit_staff_save,name="edit_staff_save"),
    path('edit_accountant_save', HodViews.edit_accountant_save,name="edit_accountant_save"),
    path('edit_student/<str:student_id>', HodViews.edit_student,name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save,name="edit_student_save"),
    path('edit_subject/<str:subject_id>', HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_course/<str:course_id>', HodViews.edit_course,name="edit_course"),
    path('edit_course_save', HodViews.edit_course_save,name="edit_course_save"),
    path('manage_session', HodViews.manage_session,name="manage_session"),
    path('add_session_save', HodViews.add_session_save,name="add_session_save"),
    path('check_email_exist', HodViews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist,name="check_username_exist"),
    path('student_feedback_message', HodViews.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replied', HodViews.student_feedback_message_replied,name="student_feedback_message_replied"),
    path('staff_feedback_message', HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('student_leave_view', HodViews.student_leave_view,name="student_leave_view"),
    path('staff_leave_view', HodViews.staff_leave_view,name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>', HodViews.student_approve_leave,name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', HodViews.student_disapprove_leave,name="student_disapprove_leave"),
    path('staff_disapprove_leave/<str:leave_id>', HodViews.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave,name="staff_approve_leave"),
    path('admin_view_attendance', HodViews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendance_dates', HodViews.admin_get_attendance_dates,name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', HodViews.admin_get_attendance_student,name="admin_get_attendance_student"),
    path('admin_profile', HodViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', HodViews.admin_profile_save,name="admin_profile_save"),
    path('admin_send_notification_staff', HodViews.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('admin_send_notification_account', HodViews.admin_send_notification_account,name="admin_send_notification_account"),
    path('admin_send_notification_student', HodViews.admin_send_notification_student,name="admin_send_notification_student"),
    path('send_student_notification', HodViews.send_student_notification,name="send_student_notification"),
    path('send_staff_notification', HodViews.send_staff_notification,name="send_staff_notification"),
    path('send_account_notification', HodViews.send_account_notification,name="send_account_notification"),

    #     Staff URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save, name="staff_fcmtoken_save"),
    path('staff_all_notification', StaffViews.staff_all_notification, name="staff_all_notification"),
    path('staff_add_result', StaffViews.staff_add_result, name="staff_add_result"),
    path('save_student_result', StaffViews.save_student_result, name="save_student_result"),
    path('edit_student_result',EditResultViewClass.as_view(), name="edit_student_result"),
    path('fetch_result_student',StaffViews.fetch_result_student, name="fetch_result_student"),
    path('start_live_classroom',StaffViews.start_live_classroom, name="start_live_classroom"),
    path('start_live_classroom_process',StaffViews.start_live_classroom_process, name="start_live_classroom_process"),

    #     accountant URL Path
    path('accountant_home', AccountantView.accountant_home, name="accountant_home"),
    path('get_students', AccountantView.get_students, name="get_students"),
    path('accountant_apply_leave', AccountantView.accountant_apply_leave, name="accountant_apply_leave"),
    path('accountant_apply_leave_save', AccountantView.accountant_apply_leave_save, name="accountant_apply_leave_save"),
    path('accountant_feedback', AccountantView.accountant_feedback, name="accountant_feedback"),
    path('accountant_feedback_save', AccountantView.accountant_feedback_save, name="accountant_feedback_save"),
    path('accountant_profile', AccountantView.accountant_profile, name="accountant_profile"),
    path('accountant_profile_save', AccountantView.accountant_profile_save, name="accountant_profile_save"),
    path('accountant_fcmtoken_save', AccountantView.accountant_fcmtoken_save, name="accountant_fcmtoken_save"),
    path('accountant_all_notification', AccountantView.accountant_all_notification, name="accountant_all_notification"),
    path('list_student_fee', AccountantView.list_student_fee, name="list_student_fee"),
    path('update_student_fee/<int:student_id>/', AccountantView.update_student_fee, name="update_student_fee"),
    path('update_student_fee_save', AccountantView.update_student_fee_save, name="update_student_fee_save"),
    
    # student URl path
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('student_fcmtoken_save', StudentViews.student_fcmtoken_save, name="student_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('student_all_notification',StudentViews.student_all_notification,name="student_all_notification"),
    path('student_view_result',StudentViews.student_view_result,name="student_view_result"),
    path('join_class_room/<int:subject_id>/<int:session_year_id>',StudentViews.join_class_room,name="join_class_room"),
    path('node_modules/canvas-designer/widget.html',StaffViews.returnHtmlWidget,name="returnHtmlWidget"),
    path('fee_logs', StudentViews.get_student_fee_logs, name='fee_logs'),
    path('testurl/',views.Testurl),
    path('get_session_years/', AccountantView.get_session_years, name='get_session_years'),
    path('get_course/', AccountantView.get_course, name='get_course'),
    path('filter_students/', AccountantView.get_students, name='filter_students'),
    path('search_students/', AccountantView.search_students, name='search_students'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
