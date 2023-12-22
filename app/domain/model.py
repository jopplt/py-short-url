class Entity:
    pass


class ShortUrlEntity(Entity):
    def __init__(self, original_url: str):
        self.original_url = original_url
        self.code = self._generate_short_code(url=original_url)

    @staticmethod
    def _generate_short_code(url: str) -> str:
        import base64
        import hashlib
        import re

        return re.sub(
            r"[^\w\d]",
            "",
            base64.urlsafe_b64encode(
                hashlib.sha256(f"{url}".encode()).digest()
            ).decode(),
        )[:6].lower()
