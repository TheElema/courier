# -*- coding: utf-8 -*-
import logging
import requests

from json import dumps

from .constants import FB_URL,FB_USER_URL, HEADERS_JSON
from .errors import CourierRequestError

def serialize_(payload):

    if isinstance(payload, list):
        payload = list(map(serialize_, payload))

    if isinstance(payload, dict):
        for item in payload:
            payload[item] = serialize_(payload[item])

    if hasattr(payload, 'to_json'):
        payload = serialize_(payload.to_json())

    return payload

class Messenger:
    """
    Class that represents a singleton used to send messages to the Facebook API

    """

    def __init__(self, token='{}'):
        """
            constants use {} for interpolation, using {} allows url to remain okay
            if token is not provided on initialization.
        """
        self._token = token
        self.post_url = FB_URL.format(self._token)
        self.user_url = FB_USER_URL.format(self._token)


    @property
    def token(self):
        return self._token


    @token.setter
    def token(self, value):
        self._token = value


    def send(self, obj):
        """
        send() : takes a payload and sends it to the API
                 returns tuple of (HTTP_STATUS_CODE, HTTP_STATUS_TEXT)

        payload: message should be propery formatted JSON dict/string

        """
        # Serialize, dump to json and send back

        payload = serialize_(obj)
        payload = dumps(payload)

        try:
            status = requests.post(self.post_url, data=payload, headers=HEADERS_JSON)
        except requests.exceptions.RequestException as e:
            raise CourierRequestError(str(e))
        finally:
            return (status.status_code, status.text)


    def get_user_profile(self, fbid):
        """
        returns a tuple of the status code and a dict of the user (HTTP_STATUS_CODE, user)
            
        """
        url = self.user_url % fbid
        try:
            status = requests.get(url)
        except requests.exceptions.RequestException as e:
            raise CourierRequestError(str(e))
        finally:
            return (status.status_code, status.json())



        