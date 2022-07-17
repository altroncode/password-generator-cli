"""Module for managing dynamic app data"""
from data import base_data_model
from data._field import Field


class PasswordInfo(base_data_model.BaseModel):
    """Data for whole project"""

    _section_name: str = 'password_info'

    platform: str = Field()
    login: str = Field()
    emails: list[str] = Field()
    is_note: bool = Field()
    note: str = Field(init=False)


class Telegram(base_data_model.BaseModel):
    """Data for work with telegram"""

    _section_name: str = 'telegram'

    user_id: int = Field()
    token: str = Field()
    last_message_id: int = Field()
