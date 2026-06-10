from os.path import splitext
from threading import Thread

from django.contrib import messages
from django.contrib.auth import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from ippanel import Client


def get_timesince_persian(time):
    if not time:
        return ""

    diff = timezone.now() - time

    seconds = int(diff.total_seconds())

    intervals = (
        (31536000, _("years ago")),
        (2592000, _("months ago")),
        (86400, _("days ago")),
        (3600, _("hours ago")),
        (60, _("minutes ago")),
    )

    for interval_seconds, label in intervals:
        value = seconds // interval_seconds

        if value:
            return f"{value} {label}"

    return _("Moments ago")


# Get time in format
def get_time(frmt: str = "%Y-%m-%d %H:%M"):
    now = timezone.now()
    if frmt is not None:
        now = now.strftime(frmt)

    return now


# Create image/file path based on time
def upload_file_src(instance, path):
    now = get_time("%Y-%m-%d")
    return f"files/{now}/{path}"


# Return file extension
def get_file_extension(file_name):
    name, extension = splitext(file_name.file.name)
    return extension


# Form validator utils
def validate_form(request, form):
    if form.is_valid():
        return True

    errors = form.errors.items()

    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for field, message in errors:  # noqa: B007
        for error in message:
            messages.error(request, error)

    return False


# Toast form errors utils
def toast_form_errors(request, form):
    errors = form.errors.items()
    if not errors:
        messages.error(request, _("Entered data is not correct."))
        return False

    for field, message in errors:  # noqa: B007
        for error in message:
            messages.error(request, error)


# Get coded phone number(IR)
def get_coded_phone_number(number):
    try:
        phone_number = str(number)
        return "+98" + phone_number[1:]
    except (TypeError, IndexError):
        return None


# TODO: import djangoQ after test
# Send SMS util
def send_sms(phone_number, pattern, **kwargs):
    phone_number = get_coded_phone_number(phone_number)
    phone_number = phone_number.replace("+", "")

    # Create client instance
    sms = Client(settings.SMS_CONFIG["API_KEY"])

    # Send sms via ippanel module
    t1 = Thread(
        target=sms.send_pattern,
        args=(
            pattern,  # pattern code
            settings.SMS_CONFIG["ORIGINATOR"],  # originator
            phone_number,  # recipient
            kwargs,  # pattern values
        ),
    )
    t1.start()
