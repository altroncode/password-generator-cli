import contextlib
import http.client
import json
import typing
import urllib.error
import urllib.parse
import urllib.request

import exceptions
import utils
from config import settings
from strorages import base_storage


MessageStyles = typing.Literal['bold', 'italic', 'code', 'strike', 'underline']


def send_http_request(url: str, data: bytes) -> http.client.HTTPResponse:
    return urllib.request.urlopen(url, data)


class TelegramStorage(base_storage.BaseStorage):

    def __init__(self, telegram_settings: settings.TelegramSettings) -> None:
        self.__settings = telegram_settings
        self.__base_url = f'https://api.telegram.org/bot{self.__settings.token}'

    def keep(self, password: str, password_info: str) -> None:
        try:
            self._delete_closing_message()
            self._send_message(password_info)
            self._send_message(f'`{utils.escape_message(password)}`')
        except urllib.error.HTTPError as e:
            raise exception.SavingPasswordError from e
        finally:
            self._send_closing_message()

    def _send_closing_message(self) -> http.client.HTTPResponse:
        message = '*' * 42
        response = self._send_message(f'`{utils.escape_message(message)}`')
        self.__settings.last_message_id = str(json.loads(response.read())['result']['message_id'])
        self.__settings['last_message_id'].save()
        return response

    def _delete_closing_message(self) -> http.client.HTTPResponse | None:
        closing_message_id = self.__settings.last_message_id
        if closing_message_id is not None:
            with contextlib.suppress(urllib.error.URLError):
                url = f'{self.__base_url}/deleteMessage'
                request_data = self._prepare_request_data(
                    self.__settings.user_id, message_id=self.__settings.last_message_id
                )
                return send_http_request(url, request_data)
        return None

    def _send_message(self, message: str) -> http.client.HTTPResponse:
        url = f'{self.__base_url}/sendMessage'
        data = self._prepare_request_data(self.__settings.user_id, message)
        return send_http_request(url, data)

    @staticmethod
    def _prepare_request_data(chat_id: int, text: str = "", **kwargs) -> bytes:
        data = {
            "text": text,
            "parse_mode": "MarkdownV2",
            "chat_id": chat_id
        }
        return urllib.parse.urlencode(data | kwargs).encode("utf-8")
