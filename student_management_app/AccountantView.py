from .models import Students, Fee
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
import json
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.forms import FeeUpdateForm
from student_management_app.models import *


def accountant_home(request):
    # For Fetch All Student Under Staff
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    # removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.all().count()
    students_with_nodues_count = Students.objects.filter(
        fee__is_fee_paid=True
    ).count()
    students_with_dues_count = Students.objects.filter(
        fee__is_fee_paid=False
    ).count()
    
    
    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(
        subject_id__in=subjects).count()

    # Fetch All Approve Leave
    staff = Accountant.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(
        staff_id=staff.id, leave_status=1).count()
    subject_count = subjects.count()

    # Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(
            subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(
            status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(
            status=False, student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request, "accountant/accountant_home_template.html", {'students_with_nodues_count': students_with_nodues_count, "students_count": students_count, "attendance_count": attendance_count, "leave_count": leave_count, "subject_count": subject_count, "subject_list": subject_list,
                   "attendance_list": attendance_list, "student_list": student_list, "present_list": student_list_attendance_present, "absent_list": student_list_attendance_absent, 'students_with_dues_count': students_with_dues_count})


from datetime import datetime

def get_session_years(request):
    session_years = SessionYearModel.objects.all().values_list('id', 'session_start_year', 'session_end_year')
    session_years_list = [
        {
            'id': id,
            'text': f'{datetime.strftime(session_start_year, "%b-%d, %Y")} To {datetime.strftime(session_end_year, "%b-%d, %Y")}'
        }
        for id, session_start_year, session_end_year in session_years
    ]
    return JsonResponse(session_years_list, safe=False)


def get_course(request):
    courses = Courses.objects.all().values_list('id', 'course_name')
    course_list = [{'id': id, 'text': f'{course_name}'} for id, course_name  in courses]
    return JsonResponse(course_list, safe=False)


from django.http import JsonResponse
from django.db.models import Q

@csrf_exempt
def search_students(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term')

        students = Students.objects.filter(
            Q(admin__first_name__icontains=search_term) |
            Q(admin__last_name__icontains=search_term)
        )
        student_data = []
        for student in students:
            fees = Fee.objects.filter(student=student)
            total_amount = sum(fee.total_fee for fee in fees)
            amount_paid = sum(fee.amount_paid for fee in fees)
            if fees:
                due_date = max(fee.last_due_date for fee in fees if fee.last_due_date is not None)
            else:
                due_date = None 
            profile_pic_url = student.profile_pic.url if student.profile_pic else ''
                
            data = {
                    'id':student.id,
                    'admin.first_name': student.admin.first_name,
                    'admin.last_name': student.admin.last_name,
                    'admin.email': student.admin.email,
                    'address': student.address,
                    'gender': student.gender,
                    'session_year': f'{datetime.strftime(student.session_year_id.session_start_year, "%b-%d, %Y")} To {datetime.strftime(student.session_year_id.session_end_year, "%b-%d, %Y")}',
                    'course_name': student.course_id.course_name,
                    'date_joined': student.admin.date_joined,
                    'total_amount': total_amount,
                    'amount_paid': amount_paid,
                    'last_due_date': due_date,
                    'profile_pic': profile_pic_url,
                }
            student_data.append(data)
            return JsonResponse(student_data, safe=False)
    return JsonResponse([], safe=False)


from django.http import JsonResponse
from .models import Students, SessionYearModel, Courses

@csrf_exempt
def get_students(request):
    if request.method == 'POST':
        course_id = request.POST.get("course")
        session_year = request.POST.get("session_year")
        try:
            subject = Courses.objects.get(id=course_id)
            session_year = SessionYearModel.objects.get(id=session_year)
            students = Students.objects.filter(
                course_id=subject, session_year_id=session_year)
            
            student_data = []

            for student in students:
                # Get related Fee objects for the student
                fees = Fee.objects.filter(student=student)
                total_amount = sum(fee.total_fee for fee in fees)
                amount_paid = sum(fee.amount_paid for fee in fees)
                if fees:
                    due_date = max(fee.last_due_date for fee in fees if fee.last_due_date is not None)
                else:
                    due_date = None 
                profile_pic_url = student.profile_pic.url if student.profile_pic else ''
                
                data = {
                    'id':student.id,
                    'admin.first_name': student.admin.first_name,
                    'admin.last_name': student.admin.last_name,
                    'admin.email': student.admin.email,
                    'address': student.address,
                    'gender': student.gender,
                    'session_year': f'{datetime.strftime(student.session_year_id.session_start_year, "%b-%d, %Y")} To {datetime.strftime(student.session_year_id.session_end_year, "%b-%d, %Y")}',
                    'course_name': student.course_id.course_name,
                    'date_joined': student.admin.date_joined,
                    'total_amount': total_amount,
                    'amount_paid': amount_paid,
                    'last_due_date': due_date,
                    'profile_pic': profile_pic_url,
                }
                student_data.append(data)
            
            return JsonResponse(student_data, safe=False)
        except (Courses.DoesNotExist, SessionYearModel.DoesNotExist):
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)


def accountant_apply_leave(request):
    account_obj = Accountant.objects.get(admin=request.user.id)
    leave_data = LeaveReportAccount.objects.filter(accountant_id=account_obj)
    return render(request, "accountant/accountant_apply_leave.html", {"leave_data": leave_data})


def accountant_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("accountant_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        staff_obj = Accountant.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportAccount(
                accountant_id=staff_obj, leave_date=leave_date, leave_message=leave_msg, leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("accountant_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("accountant_apply_leave"))


def accountant_feedback(request):
    staff_id = Accountant.objects.get(admin=request.user.id)
    feedback_data = FeedBackAccountant.objects.filter(accountant_id=staff_id)
    return render(request, "accountant/accountant_feedback.html", {"feedback_data": feedback_data})


def accountant_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("accountant_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        staff_obj = Accountant.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackAccountant(
                accountant_id=staff_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("accountant_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("accountant_feedback"))


def accountant_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    account = Accountant.objects.get(admin=user)
    return render(request, "accountant/accountant_profile.html", {"user": user, "staff": account})


def accountant_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Accountant.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("accountant_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("accountant_profile"))


@csrf_exempt
def accountant_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Accountant.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def accountant_all_notification(request):
    staff = Accountant.objects.get(admin=request.user.id)
    notifications = NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request, "accountant/all_notification.html", {"notifications": notifications})


def returnHtmlWidget(request):
    return render(request, "widget.html")


def list_student_fee(request):
    students_with_fees = Students.objects.select_related(
        'admin').prefetch_related('fee_set').all()
    return render(request, 'accountant/list_students.html', {'students': students_with_fees})


def update_student_fee(request, student_id):
    student = get_object_or_404(Students, pk=student_id)
    stud_fee = None
    try:
        stud_fee = Fee.objects.get(student=student)
    except Fee.DoesNotExist:
        pass
    if request.method == "POST":
        total_fee = Decimal(request.POST.get('total_fee', 0))
        due_date = request.POST.get('due_date')
        pay_amount = Decimal(request.POST.get('pay_amount', 0))

        if due_date == "":
            due_date = None
        try:
            if stud_fee:
                stud_fee.total_fee = total_fee
                stud_fee.last_due_date = due_date
                stud_fee.amount_paid += pay_amount
                if stud_fee.amount_paid > stud_fee.total_fee:
                    messages.error(
                        request, f"Amount paid exceeded total fee!!")
                    return HttpResponseRedirect(reverse("update_student_fee", kwargs={"student_id": student.id}))
                stud_fee.save()
            else:
                # Create a new fee object if it doesn't exist
                fee = Fee.objects.create(
                    student=student,
                    total_fee=total_fee,
                    amount_paid=pay_amount,
                    last_due_date=due_date
                )
                fee.save()
        except Exception as e:
            messages.error(request, f"Error updating fee: {str(e)}")
            return HttpResponseRedirect(reverse("update_student_fee", kwargs={"student_id": student.id}))
        else:
            messages.success(request, "Fee Updated successfully")

        return HttpResponseRedirect(reverse("update_student_fee", kwargs={"student_id": student.id}))

    return render(request, 'accountant/update_student_fee.html', {'student': student, 'stud_fee': stud_fee})


def update_student_fee_save(request):
    if request.method == "POST":
        form = FeeUpdateForm(request.POST)
        if form.is_valid():
            fee_instance = form.save(commit=False)
            if fee_instance.amount_paid == fee_instance.total_fee:
                fee_instance.is_fee_paid = True
            fee_instance.save()
            messages.success(request, "Fee Updated Sucessfully")
            return redirect('list_student_fee')
        else:
            messages.error(request, "form is not valid")
            return HttpResponseRedirect(reverse("update_student_fee"))
