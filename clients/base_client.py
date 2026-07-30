import httpx


class BaseClient:
    """
    Base class for all clients.
    """

    def __init__(self, client: httpx.Client):
        self.client = client

    def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        response = self.client.request(method, endpoint, **kwargs)

        # response.raise_for_status()

        return response
