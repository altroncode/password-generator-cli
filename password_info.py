import typing

from data import app_data


class BasePasswordInfoBuilder(typing.Protocol):

    def get_password_info(self) -> str:
        pass

    def set_platform(self, platform: str) -> str:
        pass

    def set_username(self, username: str) -> str:
        pass

    def set_email(self, email: str) -> str:
        pass

    def set_note(self, note: str) -> str:
        pass


class TelegramPasswordInfoBuilder:

    def __init__(self):
        self._password_info = ''

    def get_password_info(self) -> str:
        return self._password_info

    def set_platform(self, platform: str) -> str:
        self._password_info += f'\nPlatform: {platform}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_username(self, username: str) -> str:
        self._password_info += f'\nUsername: {username}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_email(self, email: str) -> str:
        self._password_info += f'\nEmail: {email}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_note(self, note: str) -> str:
        self._password_info += f'\nNote: {note}'
        self._password_info.lstrip('\n')
        return self._password_info


class PasswordInfoDirector:
    def __init__(self, data: app_data.PasswordInfoData):
        self._data = data

    def create_password_info(self, builder: BasePasswordInfoBuilder):
        platform = self._data.platform
        username = self._data.username
        note = self._data.note
        if platform is not None:
            builder.set_platform(platform)
        if username is not None:
            builder.set_username(username)
        for email in self._data.emails:
            builder.set_email(email)
        if note is not None:
            builder.set_note(note)

        return builder.get_password_info()
