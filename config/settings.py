from config.data_models import base_data_model
from config.data_models.field import Field

SETTINGS_PATH = 'password-generator/config/settings.ini'
ENV_PATH = 'password-generator/.env'


class AppSettings(base_data_model.BaseModel):
    _sections: tuple[str] = ('app',)

    storages: list[str] = Field()


class CredentialsSettings(base_data_model.BaseModel):
    _sections: str = ('password_info',)

    platform: str = Field(env='PLATFORM')
    login: str = Field(env='LOGIN')
    emails: list[str] = Field(env='EMAILS')
    is_note: bool = Field(env='IS_NOTE')
    note: str = Field(init=False)


class TelegramSettings(base_data_model.BaseModel):
    _sections: tuple[str] = ('telegram',)

    user_id: int = Field(env='USER_ID')
    token: str = Field(env='TOKEN')
    last_message_id: int = Field(env='LAST_MESSAGE_ID')


class PasswordSettings(base_data_model.BaseModel):
    _sections: tuple[str] = ('password',)

    length: int = Field()
    is_digits: bool = Field()
    is_capital_letters: bool = Field()
    is_small_letters: bool = Field()
    is_punctuation: bool = Field()
