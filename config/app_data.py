"""Module for managing dynamic app config"""
from config import base_data_model
from config._field import Field


class PasswordInfoData(base_data_model.BaseModel):
    """Data for whole project"""

    _section_name: str = 'password_info'

    platform: str = Field()
    login: str = Field()
    emails: list[str] = Field()
    is_note: bool = Field()
    note: str = Field(init=False)


class TelegramData(base_data_model.BaseModel):
    """Data for work with telegram"""

    _section_name: str = 'telegram'

    user_id: int = Field()
    token: str = Field()
    last_message_id: int = Field()
