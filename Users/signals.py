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


@receiver(post_save, sender=JobApplication)
def job_application_status_change(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # Skip notifications when the object is first created
        return

    # Check if the status has changed
    if instance.tracker.has_changed('status'):
        Notification.objects.create(
            recipient=instance.user_profile.user,
            message=f'Your application for {instance.job.title} has been {instance.status}.'
        )