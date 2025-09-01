import re

from bs4 import BeautifulSoup

from .client import FunPayClient
from .models import Profile


class ProfileParser:
    def __init__(self) -> None:
        self.client = FunPayClient()
    
    def parse_profile(self, profile_id: int) -> Profile:
        """Parses user profile data from HTML and returns Profile object
    
        Retrieves profile HTML, extracts user information including name,
        avatar, online status, registration date, and review statistics.
        
        Args:
            profile_id (int): The unique identifier of the user profile
        
        Returns:
            Profile: Profile object containing parsed user data with fields:
                id, avatar_url, name, login_time, registration_date,
                reviews_count, recent_reviews
        """
        html = self.client.get_profile_html(profile_id)
        soup = BeautifulSoup(html, 'html.parser')
        
        name_tag = soup.select_one('.profile h1 span.mr4')
        name = name_tag.text.strip() if name_tag else 'Unknown'

        avatar_tag = soup.select_one('.avatar-photo')
        avatar_url = ''
        if avatar_tag:
            style_attr = avatar_tag.get('style', '')
            if isinstance(style_attr, str):
                match = re.search(r'url\((.*?)\)', style_attr)
                if match:
                    avatar_url = match.group(1)
                    if avatar_url == '/img/layout/avatar.png':  
                       avatar_url = 'https://funpay.com/img/layout/avatar.png'
                    

        online_tag = soup.select_one('.media-user-status')
        login_time = online_tag.text.strip() if online_tag else 'Unknown'

        reg_tag = soup.select_one(
            '.profile-header-cols .param-item .text-nowrap'
        )
        registration_date = ''
        if reg_tag:
            registration_date = reg_tag.text.strip().split("\n")[0].strip()

        reviews_tag = soup.select_one('.text-mini.text-light.mb5')
        reviews_count = 0
        recent_reviews = 0
        if reviews_tag:
            text = reviews_tag.text.strip()
            match = re.search(r'(\d+)\s+отзыв[а-я]* за (\d+)', text)
            if match:
                reviews_count = int(match.group(1))
                recent_reviews = int(match.group(2))

        return Profile(
            id=profile_id,
            avatar_url=avatar_url,
            name=name,
            login_time=login_time,
            registration_date=registration_date,
            reviews_count=reviews_count,
            recent_reviews=recent_reviews
        )