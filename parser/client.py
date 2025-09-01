import requests

from .config import PROFILE_URL, HEADERS
from .types import HTML
from .exceptions import FunPayClientError, ProfileNotFoundError


class FunPayClient:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
    
    def get_profile_html(self, profile_id: int) -> HTML:
        """Retrieves HTML content of a user profile page

        Args:
            profile_id (int): The profile identifier of the user

        Raises:
            ProfileNotFoundError: Raised when profile with specified ID is not found
            FunPayClientError: Raised when HTTP request error occurs (except 404)

        Returns:
            HTML: HTML object containing the profile page content
        """
        url = f'{PROFILE_URL}/{profile_id}/'
        response = self.session.get(url)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 404:
                raise ProfileNotFoundError(
                    f"Profile '{profile_id}' not found."
                ) from e
            else:
                raise FunPayClientError(
                    f"Request error: {response.status_code}."
                ) from e
        return HTML(response.text)