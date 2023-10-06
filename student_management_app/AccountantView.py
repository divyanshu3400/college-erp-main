import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.forms import FeeUpdateForm
from student_management_app.models import *


def accountant_home(request):
    #For Fetch All Student Under Staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    staff=Accountant.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"accountant/accountant_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def accountant_apply_leave(request):
    account_obj = Accountant.objects.get(admin=request.user.id)
    leave_data=LeaveReportAccount.objects.filter(accountant_id=account_obj)
    return render(request,"accountant/accountant_apply_leave.html",{"leave_data":leave_data})

def accountant_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("accountant_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Accountant.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportAccount(accountant_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("accountant_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("accountant_apply_leave"))


def accountant_feedback(request):
    staff_id=Accountant.objects.get(admin=request.user.id)
    print("Accountant Id: ",staff_id)
    feedback_data=FeedBackAccountant.objects.filter(accountant_id=staff_id)
    return render(request,"accountant/accountant_feedback.html",{"feedback_data":feedback_data})

def accountant_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("accountant_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Accountant.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackAccountant(accountant_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("accountant_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("accountant_feedback"))

def accountant_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    account=Accountant.objects.get(admin=user)
    return render(request,"accountant/accountant_profile.html",{"user":user,"staff":account})

def accountant_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Accountant.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("accountant_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("accountant_profile"))

@csrf_exempt
def accountant_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Accountant.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def accountant_all_notification(request):
    staff=Accountant.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"accountant/all_notification.html",{"notifications":notifications})

def returnHtmlWidget(request):
    return render(request,"widget.html")


from django.shortcuts import render, redirect


def list_student_fee(request):
    students_with_fees = Students.objects.select_related('admin').prefetch_related('fee_set').all()
    return render(request, 'accountant/list_students.html', {'students': students_with_fees})

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

def update_student_fee(request, student_id):
    student = get_object_or_404(Students, pk=student_id)
    if request.method == "POST":
        total_fee = request.POST.get('total_fee')
        amount_paid = request.POST.get('amount_paid')
        due_date = request.POST.get('due_date')
        id = request.POST.get('student_id')
        stud = Students.objects.get(id=id)
        print(total_fee)
        print(amount_paid)
        print(due_date)
        print(id)
        try:
            fee = Fee.objects.get(student=stud)
            fee.total_fee = total_fee
            fee.amount_paid = amount_paid
            fee.due_date = due_date
            fee.save()
        except Fee.DoesNotExist:
            fee = Fee.objects.create(student=stud,total_fee=total_fee,amount_paid=amount_paid,due_date=due_date)
            fee.save()
        messages.success(request,"Fee Updated successfully")
        return HttpResponseRedirect(reverse("update_student_fee",kwargs={"student_id":stud.id}))

    return render(request, 'accountant/update_student_fee.html', {'student': student})



def update_student_fee_save(request):
    if request.method == "POST":
        form =FeeUpdateForm(request.POST)
        if form.is_valid():
            fee_instance = form.save(commit=False)
            if fee_instance.amount_paid == fee_instance.total_fee:
                fee_instance.is_fee_paid = True
            fee_instance.save()
            messages.success(request, "Fee Updated Sucessfully")
            return redirect('list_student_fee')
        else:
            messages.error(request,"form is not valid")
            return HttpResponseRedirect(reverse("update_student_fee"))