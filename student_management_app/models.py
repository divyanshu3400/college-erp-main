from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    objects=models.Manager()
    
    def __str__(self):
        return f'{self.session_start_year} + {self.session_end_year}'
    
    class Meta:
        db_table = 'tbl_session_year'
        managed = True
        verbose_name = 'SessionYear'
        verbose_name_plural = 'SessionYears'

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"),(4,"Accountant"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    
    class Meta:
        db_table = 'tbl_user'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
        
class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
    class Meta:
        db_table = 'tbl_admin_hod'
        managed = True
        verbose_name = 'AdminHOD'
        verbose_name_plural = 'AdminHODs'

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    is_coordinator = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name

    class Meta:
        db_table = 'tbl_admin_staff'
        managed = True
        verbose_name = 'Staffs'
        verbose_name_plural = 'Staffs'



class Accountant(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name
    
    class Meta:
        db_table = 'tbl_admin_accountant'
        managed = True
        verbose_name = 'Accountant'
        verbose_name_plural = 'Accountants'


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
   
    def __str__(self):
        return self.course_name
    
    class Meta:
        db_table = 'tbl_courses'
        managed = True
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name
    
    class Meta:
        db_table = 'tbl_subjects'
        managed = True
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField(upload_to='student_profile_pic/')
    address=models.TextField()
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects = models.Manager()

    def __str__(self):
        return self.admin.first_name
    
    class Meta:
        db_table = 'tbl_student'
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Examination(models.Model):
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    semester = models.IntegerField()
    examination_date = models.DateField()
    admit_card = models.FileField(upload_to='admit_cards/')
    students = models.ManyToManyField(Students, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"Examination for Semester {self.semester} - {self.session_year_id}"

    class Meta:
        db_table = 'tbl_examination'
        managed = True
        verbose_name = 'Examination'
        verbose_name_plural = 'Examinations'


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return self.attendance_date
        
    class Meta:
        db_table = 'tbl_attendance'
        managed = True
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
    def __str__(self):
        return f'{self.student_id.admin.first_name} : {self.attendance_id.attendance_date}'
        
    class Meta:
        db_table = 'tbl_attendance_report'
        managed = True
        verbose_name = 'AttendanceReport'
        verbose_name_plural = 'AttendanceReports'

from decimal import Decimal
class Fee(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True)
    receipt = models.FileField(upload_to='fee_receipts/')
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    is_fee_paid = models.BooleanField(default=False)
    due_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    pay_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    last_due_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Convert string representations to Decimal
        self.total_fee = Decimal(self.total_fee)
        self.amount_paid = Decimal(self.amount_paid)
        self.pay_amount = Decimal(self.pay_amount)

        if self.amount_paid == self.total_fee:
            self.is_fee_paid = True
        self.amount_paid += self.pay_amount 
        self.due_amount = self.total_fee - self.amount_paid
        self.pay_amount = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student.admin.first_name} : {self.amount_paid}'
        
    class Meta:
        db_table = 'tbl_fee'
        managed = True
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'

class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
    def __str__(self):
        return f'{self.student_id.admin.first_name} : {self.leave_date} :{self.leave_status} '
        
    class Meta:
        db_table = 'tbl_leave_report_student'
        managed = True
        verbose_name = 'LeaveReportStudent'
        verbose_name_plural = 'LeaveReportStudents'

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return f'{self.staff_id.admin.first_name} : {self.leave_date} :{self.leave_status} '
        
    class Meta:
        db_table = 'tbl_leave_report_staff'
        managed = True
        verbose_name = 'LeaveReportStaff'
        verbose_name_plural = 'LeaveReportStaffs'

class LeaveReportAccount(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return f'{self.accountant_id.admin.first_name} : {self.leave_date} :{self.leave_status} '
        
    class Meta:
        db_table = 'tbl_leave_report_account'
        managed = True
        verbose_name = 'LeaveReportAccount'
        verbose_name_plural = 'LeaveReportAccount'


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 
    def __str__(self):
        return f'{self.student_id.admin.first_name} : {self.feedback} :Reply- {self.feedback_reply} '
        
    class Meta:
        db_table = 'tbl_feedback_student'
        managed = True
        verbose_name = 'FeedBackStudent'
        verbose_name_plural = 'FeedBackStudents'


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.staff_id.admin.first_name} : {self.feedback} :Reply- {self.feedback_reply} '
        
    class Meta:
        db_table = 'tbl_feedback_staff'
        managed = True
        verbose_name = 'FeedBackStaffs'
        verbose_name_plural = 'FeedBackStaffs'
        
class FeedBackAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.accountant_id.admin.first_name} : {self.feedback} :Reply- {self.feedback_reply} '
        
    class Meta:
        db_table = 'tbl_feedback_acccount'
        managed = True
        verbose_name = 'FeedBackAccount'
        verbose_name_plural = 'FeedBackAccount'


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.student_id.admin.first_name} :Message- {self.message}'
        
    class Meta:
        db_table = 'tbl_notification_student'
        managed = True
        verbose_name = 'NotificationStudent'
        verbose_name_plural = 'NotificationStudents'



class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return f'{self.staff_id.admin.first_name} :Message- {self.message}'
        
    class Meta:
        db_table = 'tbl_notification_staff'
        managed = True
        verbose_name = 'NotificationStaff'
        verbose_name_plural = 'NotificationStaffs'


class NotificationAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    def __str__(self):
        return f'{self.accountant_id.admin.first_name} :Message- {self.message}'
        
    class Meta:
        db_table = 'tbl_notification_accountant'
        managed = True
        verbose_name = 'NotificationStaff'
        verbose_name_plural = 'NotificationStaffs'


class StudentResult(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    subject_exam_marks=models.FloatField(default=0)
    subject_assignment_marks=models.FloatField(default=0)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return f'{self.student_id.admin.first_name} :Subject- {self.subject_id.subject_name}: Marks(Assignment-{self.subject_assignment_marks} + Exam-{self.subject_exam_marks}) '
        
    class Meta:
        db_table = 'tbl_student_result'
        managed = True
        verbose_name = 'StudentResult'
        verbose_name_plural = 'StudentResults'


class OnlineClassRoom(models.Model):
    id=models.AutoField(primary_key=True)
    room_name=models.CharField(max_length=255)
    room_pwd=models.CharField(max_length=255)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    session_years=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)
    started_by=models.ForeignKey(Staffs,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    created_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")  
        if instance.user_type==3:
            Students.objects.create(admin=instance,course_id=Courses.objects.first(),session_year_id=SessionYearModel.objects.first(),address="",profile_pic="",gender="")
        if instance.user_type==4:
            Accountant.objects.create(admin=instance,address="")
          
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()
    if instance.user_type==4:
        instance.accountant.save()
