from rest_framework.serializers import ValidationError
from urllib.parse import urlparse


def youtube_only_validator(value: str):
    """
    Разрешены только ссылки на youtube.com и youtu.be
    """
    if not value:
        return

    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be']

    if domain not in allowed_domains:
        raise ValidationError(
            'Разрешены только ссылки на видео с youtube.com'
        )
