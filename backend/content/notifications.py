import logging
import smtplib

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail

logger = logging.getLogger(__name__)


def notify_contact_inquiry(inquiry):
    """Send a plain-text heads-up; saving the inquiry remains successful if email is down."""
    if not all((
        settings.EMAIL_HOST,
        settings.EMAIL_HOST_USER,
        settings.EMAIL_HOST_PASSWORD,
        settings.CONTACT_NOTIFICATION_EMAIL,
    )):
        logger.info('Contact notification skipped: SMTP credentials or recipient are not configured.')
        return False

    project_type = inquiry.project_type or 'Project inquiry'
    subject = f'New website inquiry — {project_type}'
    body = '\n'.join([
        'A new project inquiry was submitted on Creova Studio.',
        '',
        f'Name: {inquiry.name}',
        f'Email: {inquiry.email}',
        f'Company / brand: {inquiry.company_brand or "Not provided"}',
        f'Project type: {inquiry.project_type or "Not provided"}',
        f'Budget range: {inquiry.budget_range or "Not provided"}',
        '',
        'Project details:',
        inquiry.message,
        '',
        'Open Django Admin → Form submissions to manage this lead.',
    ])

    try:
        sent_count = send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
            fail_silently=False,
            reply_to=[inquiry.email],
        )
        return sent_count > 0
    except (BadHeaderError, OSError, smtplib.SMTPException, ValueError):
        logger.exception('Could not send email notification for inquiry id=%s', inquiry.pk)
        return False
