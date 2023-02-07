import contextlib
import http.client
import json
import urllib.error
import urllib.parse
import urllib.request

import exceptions
import password
import text_processing
import utils
from config import settings
from storages import base_storage
from text_processing import html_tags


class TelegramStorage(base_storage.BaseStorage):

    def __init__(self, telegram_settings: settings.TelegramSettings) -> None:
        super().__init__(telegram_settings)
        self.__settings = telegram_settings
        self.__base_url = f'https://api.telegram.org/bot{self.__settings.token}'
        self.__text_processing = text_processing.TelegramTextProcessing()

    def keep(self, password_: password.Password, credentials: str, note: str = None) -> None:
        try:
            self._delete_closing_message()
            self._send_message(f'{credentials}\n\n{note or ""}'.rstrip('\n'))
            formatted_password = self.__text_processing.escape_text(str(password_))
            formatted_password = self.__text_processing.format_text(formatted_password, html_tags.CodeTag())
            self._send_message(formatted_password)
        except urllib.error.HTTPError as e:
            raise exceptions.SavingPasswordError from e
        finally:
            self._send_closing_message()

    def _send_closing_message(self) -> http.client.HTTPResponse:
        message = self.__text_processing.format_text('*' * 42, html_tags.CodeTag())
        response = self._send_message(message)
        self.__settings.last_message_id = str(json.loads(response.read())['result']['message_id'])
        self.__settings['last_message_id'].save()
        return response

    def _delete_closing_message(self) -> http.client.HTTPResponse | None:
        closing_message_id = self.__settings.last_message_id
        if closing_message_id is not None:
            with contextlib.suppress(urllib.error.URLError):
                url = f'{self.__base_url}/deleteMessage'
                request_data = self._prepare_request_data(
                    self.__settings.chat_id, message_id=self.__settings.last_message_id
                )
                return utils.send_http_request(url, request_data)
        return None

    def _send_message(self, message: str) -> http.client.HTTPResponse:
        url = f'{self.__base_url}/sendMessage'
        data = self._prepare_request_data(self.__settings.chat_id, message)
        return utils.send_http_request(url, data)

    @staticmethod
    def _prepare_request_data(chat_id: int, text: str = "", **kwargs) -> bytes:
        data = {
            "text": text,
            "parse_mode": "HTML",
            "chat_id": chat_id
        }
        return urllib.parse.urlencode(data | kwargs).encode("utf-8")
