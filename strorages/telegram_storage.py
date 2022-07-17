import contextlib
import json
import typing
import urllib.request
import urllib.parse
import urllib.error
import http.client

from strorages import base_storage
from data import app_data
import exception

MessageStyles = typing.Literal['bold', 'italic', 'code', 'strike', 'underline']


def send_request(url: str, data: bytes) -> http.client.HTTPResponse:
    return urllib.request.urlopen(url, data)


def escape_message(message: str) -> str:
    return "".join([f'\\{i}' for i in message])


class TelegramStorage(base_storage.BaseStorage):

    def __init__(self, data: app_data.TelegramData) -> None:
        self.data = data
        self.base_url = f'https://api.telegram.org/bot{self.data.token}'

    def keep(self, password: str, password_info: str) -> None:
        try:
            self._delete_closing_message()
            self._send_message(password_info)
            self._send_message(escape_message(password), style='code')
            self._send_closing_message()
        except urllib.error.HTTPError as e:
            raise exception.KeepPasswordError from e

    def _send_closing_message(self) -> http.client.HTTPResponse:
        message = '*' * 42
        response = self._send_message(message, style='code')
        self.data.last_message_id = str(json.loads(response.read())['result']['message_id'])
        self.data['last_message_id'].save()
        return response

    def _delete_closing_message(self) -> http.client.HTTPResponse | None:
        closing_message_id = self.data.last_message_id
        if closing_message_id is not None:
            with contextlib.suppress(urllib.error.URLError):
                url = f'{self.base_url}/deleteMessage'
                request_data = self._prepare_request_data(
                    self.data.user_id, message_id=self.data.last_message_id
                )
                return send_request(url, request_data)
        return None

    def _send_message(self, message: str, style: MessageStyles = None) -> http.client.HTTPResponse:
        url = f'{self.base_url}/sendMessage'
        style_templates = {
            'bold': '*{}*',
            'italic': '__{}__',
            'code': '`{}`',
            'strike': '~{}~',
        }
        style_template = style_templates.get(style)
        if style_template:
            message = style_template.format(message)
        data = self._prepare_request_data(self.data.user_id, message)
        return send_request(url, data)

    @staticmethod
    def _prepare_request_data(chat_id: int, text: str = "", **kwargs) -> bytes:
        data = {
            "text": text,
            "parse_mode": "MarkdownV2",
            "chat_id": chat_id
        }
        return urllib.parse.urlencode(data | kwargs).encode("utf-8")
