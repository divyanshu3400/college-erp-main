# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib import messages
from .models import Fee  # Import your Fee model here

@receiver(post_save, sender=Fee)
def check_fee_payment(sender, instance, **kwargs):
    if not instance.is_fee_paid and instance.due_date and instance.due_date > timezone.now().date():
        # Check if the amount_paid is less than the total_fee
        if instance.amount_paid < instance.total_fee:
            # Send a message to the student
            messages.warning(instance.student.admin, "Your fee payment is pending. Please pay before the due date.")
