import typing


class BasePasswordInfoBuilder(typing.Protocol):
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


class Director:
    def create_password_info(self, builder: BasePasswordInfoBuilder):
        pass
