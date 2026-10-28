import logging

from django.conf import settings
from ippanel import Client

from apps.core.utils import get_coded_phone_number


logger = logging.getLogger(__name__)


def send_sms_task(phone_number, pattern, kwargs):
    logger.info(
        "SMS TASK START | phone=%s | pattern=%s | kwargs_keys=%s",
        phone_number,
        pattern,
        list(kwargs.keys()),
    )

    try:
        coded_phone = get_coded_phone_number(phone_number)

        logger.info(
            "SMS PHONE NORMALIZED | original=%s | normalized=%s",
            phone_number,
            coded_phone,
        )

        recipient = coded_phone.replace("+", "")

        logger.info(
            "SMS CLIENT INIT | api_key_exists=%s | originator=%s",
            bool(settings.SMS_CONFIG.get("API_KEY")),
            settings.SMS_CONFIG.get("ORIGINATOR"),
        )

        sms = Client(settings.SMS_CONFIG["API_KEY"])

        logger.info(
            "SMS IPPANEL REQUEST | pattern=%s | recipient=%s | kwargs=%s",
            pattern,
            recipient,
            kwargs,
        )

        result = sms.send_pattern(
            pattern,
            settings.SMS_CONFIG["ORIGINATOR"],
            recipient,
            kwargs,
        )

        logger.info(
            "SMS IPPANEL SUCCESS | result=%s",
            result,
        )

        return result

    except Exception:
        logger.exception(
            "SMS IPPANEL FAILED | phone=%s | pattern=%s",
            phone_number,
            pattern,
        )
        raise
