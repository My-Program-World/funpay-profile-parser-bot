from pydantic import BaseModel


class Profile(BaseModel):
    """User profile data model
    
    Represents a FunPay user profile with basic information and 
    activity statistics.
    
    Attributes:
        id (int): Unique profile identifier
        avatar_url (str): URL to user's avatar image
        name (str): Display name of the user
        login_time (str): Last login time or online status
        registration_date (str): Date when user registered
        reviews_count (int): Total number of reviews received
        recent_reviews (int): Number of recent reviews in specified period
    """
    id: int
    avatar_url: str
    name: str
    login_time: str           
    registration_date: str    
    reviews_count: int
    recent_reviews: int