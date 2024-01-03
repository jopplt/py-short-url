class Entity:
    pass


class ShortUrlEntity(Entity):
    def __init__(self, original_url: str):
        self.original_url = original_url
        self.code = self._generate_short_code()

    def _generate_short_code(self) -> str:
        import base64
        import hashlib
        import re

        return re.sub(
            r"[^\w\d]",
            "",
            base64.urlsafe_b64encode(
                hashlib.sha256(f"{self.original_url}".encode()).digest()
            ).decode(),
        )[:6].lower()
