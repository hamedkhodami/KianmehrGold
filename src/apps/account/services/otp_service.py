from django.core.cache import cache


class OTPService:

    RESEND_TIMEOUT = 60

    @staticmethod
    def can_send(phone_number: str) -> bool:
        key = f"otp-lock:{phone_number}"

        return cache.get(key) is None

    @staticmethod
    def set_otp(phone_number: str, code: str, expire_seconds: int = 120):
        otp_key = f"otp:{phone_number}"
        lock_key = f"otp-lock:{phone_number}"

        cache.set(otp_key, code, timeout=expire_seconds)

        cache.set(lock_key, True, timeout=OTPService.RESEND_TIMEOUT)

    @staticmethod
    def verify_otp(phone_number: str, code: str) -> bool:

        key = f"otp:{phone_number}"

        stored_code = cache.get(key)

        if stored_code is None:
            return False

        if stored_code != code:
            return False

        cache.delete(key)

        return True

    @staticmethod
    def delete_otp(phone_number: str):
        cache.delete(f"otp:{phone_number}")
