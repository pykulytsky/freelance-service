from typing import Optional
from urllib.parse import urljoin

import requests
from django.conf import settings


class BearerAuth(requests.auth.AuthBase):
    """Base Bearer authentication"""
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["authorization"] = "Bearer " + self.token
        return request


class SendgridAuthenticationFailed(BaseException):
    pass


class SendgridWrongRequest(BaseException):
    pass


class SendgridHTTP():
    """Class-wrapper over requests, for easy operation on Sendgrid."""

    def __init__(self, api_key: Optional[str] = settings.SENDGRID_API_KEY) -> None:
        self.api_key = api_key

    @property
    def base_url(self):
        return 'https://api.sendgrid.com/v3/'

    def format_url(self, url: str):
        return urljoin(self.base_url, url.lstrip('/'))

    def request(self, url: str, data: dict, method: str):
        url = self.format_url(url)
        requests_payload = dict()
        if data is not None:
            requests_payload['json'] = data

        response = requests.request(
            method=method,
            url=url,
            auth=BearerAuth(self.api_key),
            **requests_payload
        )

        if response.status_code in [401, 403]:
            raise SendgridAuthenticationFailed(f"[{response.status_code}]Wrong api key was provided: [{str(response.json())}]")

        if response.status_code == 400:
            raise SendgridWrongRequest(f"[{response.status_code}] Error in request body: [{str(response.json())}]")

        return self.get_json(response=response)

    def get(self, url: str, data: dict):
        return self.request(url, data, 'GET')

    def post(self, url: str, data: dict):
        return self.request(url, data, 'POST')

    def delete(self, url: str, data: dict):
        return self.request(url, data, 'DELETE')

    @staticmethod
    def get_json(response):
        if len(response.text):
            return response.json()
        else:
            return {
                'status': response.status_code
            }
