class BehpardakhtService:

    @classmethod
    def request_payment(cls, payment):
        """
        send request to Behpardakht

        return:
        {
            "success": True,
            "token": "...",
        }

        """

        pass

    @classmethod
    def verify_payment(cls, payment):
        """
        verify transaction

        return:

        {
            "success":True,
            "ref_id":"...."
        }

        """

        pass
