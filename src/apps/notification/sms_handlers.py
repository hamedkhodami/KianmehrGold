from apps.core.utils import send_sms


class SMSHandlers:

    @staticmethod
    def mobile_verification(notification, phone_number):
        pattern = ""  # کد پترن OTP
        send_sms(
            phone_number,
            pattern,
            **{"verification-code": notification.kwargs["code"]},
        )

    @staticmethod
    def admin_alert(notification, phone_number):
        pattern = ""  # پترن پیامک ادمین
        send_sms(
            phone_number,
            pattern,
            **{
                "title": notification.title,
                "description": notification.description,
                "order_id": notification.kwargs.get("order_id"),
                "user_phone": notification.kwargs.get("user_phone"),
                "product": notification.kwargs.get("product"),
            },
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
