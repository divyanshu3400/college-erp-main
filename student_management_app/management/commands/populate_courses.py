from django.core.management.base import BaseCommand
from student_management_app.models import Courses

class Command(BaseCommand):
    help = 'Autopopulate Coursed in the tbl_courses'
    

    def handle(self, *args, **options):
            # Clear existing categories and subcategories
        self.stdout.write(self.style.SUCCESS('Populating courses model...'))

        Courses.objects.all().delete()
        
        courses = ['BA','BBA','BCA', 'B. COM', 'B. COM(H)','B. TECH', 'MA', 'MCA', 'M. TECH']

        for course in courses:
            brand = Courses.objects.create(course_name=course)

        self.stdout.write(self.style.SUCCESS('Categories and subcategories populated successfully.'))
