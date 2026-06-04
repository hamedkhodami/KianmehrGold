from django.core.cache import cache


class OTPService:
    @staticmethod
    def set_otp(phone_number: str, code: str, expire_seconds: int = 120):
        key = f"otp:{phone_number}"
        cache.set(key, code, timeout=expire_seconds)

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
        key = f"otp:{phone_number}"
        cache.delete(key)
