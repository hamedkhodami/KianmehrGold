from apps.notification.email_handlers import EmailHandlers
from apps.notification.enums import NotificationChannelEnum, NotificationTypeEnum
from apps.notification.inapp_handlers import InAppHandlers
from apps.notification.sms_handlers import SMSHandlers


class NotificationDispatcher:

    @staticmethod
    def dispatch(notification):
        channel = notification.channel
        user = notification.to_user

        if channel == NotificationChannelEnum.SMS:
            NotificationDispatcher._dispatch_sms(notification, user.phone_number)

        elif channel == NotificationChannelEnum.EMAIL:
            NotificationDispatcher._dispatch_email(notification)

        elif channel == NotificationChannelEnum.IN_APP:
            NotificationDispatcher._dispatch_inapp(notification)

    @staticmethod
    def _dispatch_sms(notification, phone_number):
        handlers = {
            NotificationTypeEnum.MOBILE_VERIFICATION_CODE: SMSHandlers.mobile_verification,
            NotificationTypeEnum.ADMIN_ALERT: SMSHandlers.admin_alert,
            NotificationTypeEnum.ORDER_CANCELED: SMSHandlers.order_canceled,
            NotificationTypeEnum.ORDER_CARD_TO_CARD_CONFIRMED: SMSHandlers.order_card_to_card_confirmed,
            NotificationTypeEnum.ORDER_GATEWAY_LINK: SMSHandlers.order_gateway_link,
        }

        handler = handlers.get(notification.type)
        if handler:
            handler(notification, phone_number)

    @staticmethod
    def _dispatch_email(notification):
        EmailHandlers.send_email(notification)

    @staticmethod
    def _dispatch_inapp(notification):
        InAppHandlers.create_inapp(notification)
