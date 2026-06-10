from apps.core.utils import send_sms
from apps.notification.enums import NotificationEnums


class NotificationUser:

    @classmethod
    def mobile_verification_code_handler(cls, notification, phone_number):
        pattern = "6yk1gp8ytmyk7ia"
        send_sms(
            phone_number, pattern, **{"verification-code": notification.kwargs["code"]}
        )


NOTIFICATION_USER_HANDLERS = {
    NotificationEnums.MOBILE_VERIFICATION_CODE.value: NotificationUser.mobile_verification_code_handler,
}
