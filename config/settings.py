from config.data_models import base_data_model
from config.data_models.field import Field


SETTINGS_PATH = 'password-generator/config/settings.ini'


class PasswordInfoSettings(base_data_model.BaseModel):
    _section_name: str = 'password_info'

    platform: str = Field()
    login: str = Field()
    emails: list[str] = Field()
    is_note: bool = Field()
    note: str = Field(init=False)


class TelegramSettings(base_data_model.BaseModel):
    _section_name: str = 'telegram'

    user_id: int = Field()
    token: str = Field()
    last_message_id: int = Field()


class GeneralSettings(base_data_model.BaseModel):
    _section_name = 'general'

    storages: list[str] = Field()


class PasswordSettings(base_data_model.BaseModel):
    _section_name: str = 'password'

    length: int = Field()
    is_digits: bool = Field()
    is_capital_letters: bool = Field()
    is_small_letters: bool = Field()
    is_punctuation: bool = Field()
