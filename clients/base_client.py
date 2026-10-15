import httpx


class BaseClient:
    """
    Base class for all clients.
    """

    def __init__(self, client: httpx.Client):
        self.client = client

    def _request(
        self,
        method: str,
        endpoint: str,
        headers: dict = None,
        access_token: str = None,
        **kwargs,
    ) -> httpx.Response:

        if headers is None:
            headers = {}

        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        response = self.client.request(method, endpoint, headers=headers, **kwargs)
        return response
