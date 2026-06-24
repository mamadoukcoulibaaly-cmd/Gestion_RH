import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

logger = logging.getLogger('information_employees.auth')


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    logger.info("User logged in: %s (id=%s, email=%s)", user.get_username(), user.pk, getattr(user, 'email', ''))


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    username = user.get_username() if user else 'anonymous'
    user_id = getattr(user, 'pk', 'unknown')
    logger.info("User logged out: %s (id=%s)", username, user_id)
