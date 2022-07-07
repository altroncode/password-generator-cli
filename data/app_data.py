"""Module for managing dynamic app data"""
from data import base_data_model
from data._field import Field


class PasswordInfoData(base_data_model.BaseDataModel):
    """Data for whole project"""

    _section_name: str = 'password_info'

    platform = Field(value_type=str)
    username = Field(value_type=str)
    emails = Field(value_type=list)
    note = Field(value_type=str)


class TelegramData(base_data_model.BaseDataModel):
    """Data for work with telegram"""

    _section_name: str = 'telegram'

    user_id = Field(value_type=int)
    token = Field(value_type=str)
    last_message_id = Field(value_type=int)
