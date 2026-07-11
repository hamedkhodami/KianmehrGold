from apps.core.utils import send_sms
from apps.notification.enums import NotificationEnums


class NotificationUser:

    @classmethod
    def mobile_verification_code_handler(cls, notification, phone_number):
        pattern = ""
        send_sms(
            phone_number,
            pattern,
            **{"verification-code": notification.kwargs["code"]},
        )

    @classmethod
    def wallet_transaction_handler(cls, notification, phone_number):
        pattern = ""
        send_sms(
            phone_number,
            pattern,
            **{
                "amount": notification.kwargs.get("amount"),
                "status": notification.kwargs.get("status"),
            },
        )


NOTIFICATION_USER_HANDLERS = {
    NotificationEnums.MOBILE_VERIFICATION_CODE.value: NotificationUser.mobile_verification_code_handler,
    NotificationEnums.WALLET_TRANSACTION.value: NotificationUser.wallet_transaction_handler,
}
