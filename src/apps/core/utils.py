from os.path import splitext

from django.utils import timezone
from django.utils.translation import gettext as _


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
