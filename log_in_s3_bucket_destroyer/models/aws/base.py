from models import settings


class Base:
    def endpoint_url(self) -> str:
        endpoint_url = settings.SETTINGS.get("aws_endpoint_url", None)
        endpoint_url = None if endpoint_url == "" else endpoint_url

        return endpoint_url
