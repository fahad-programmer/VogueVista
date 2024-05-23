from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import JobApplication, Notification

@receiver(post_save, sender=JobApplication)
def create_job_application_notification(sender, instance, created, **kwargs):
    if created:
        # Notify the user
        Notification.objects.create(
            recipient=instance.user_profile.user,
            message=f'You have successfully applied for {instance.job.title}.'
        )
        
        # Notify the company
        Notification.objects.create(
            recipient=instance.job.company.user,
            message=f'{instance.user_profile.user.username} has applied for {instance.job.title}.'
        )