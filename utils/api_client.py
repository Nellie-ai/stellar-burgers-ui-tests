from dataclasses import replace

import requests

from utils.constants import API_URL, DEFAULT_TIMEOUT
from utils.data import User


class StellarBurgersApi:
    """Small API client used only to prepare and clean up UI test data."""

    def __init__(self, base_url: str = API_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def create_user(self, user: User) -> User:
        response = self.session.post(
            f"{self.base_url}/api/auth/register",
            json={"email": user.email, "password": user.password, "name": user.name},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("success"):
            raise RuntimeError(f"User creation failed: {payload}")
        return replace(
            user,
            access_token=payload["accessToken"],
            refresh_token=payload["refreshToken"],
        )

    def delete_user(self, access_token: str) -> None:
        if not access_token:
            return
        response = self.session.delete(
            f"{self.base_url}/api/auth/user",
            headers={"Authorization": access_token},
            timeout=self.timeout,
        )
        if response.status_code not in (200, 202, 401, 403, 404):
            response.raise_for_status()
