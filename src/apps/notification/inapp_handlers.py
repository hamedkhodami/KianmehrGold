class InAppHandlers:

    @staticmethod
    def create_inapp(notification):
        notification.is_showing = True
        notification.save(update_fields=["is_showing"])
        return True
