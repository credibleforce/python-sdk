# -*- coding: utf-8 -*-
"""
HttpSession class for package HTTP functions.
"""

import json
import logging
import requests

from datetime import datetime, timedelta, timezone

from laceworksdk.config import (
    DEFAULT_BASE_DOMAIN,
    DEFAULT_ACCESS_TOKEN_EXPIRATION
)
from laceworksdk.exceptions import ApiError
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)


class HttpSession(object):
    """
    Package HttpSession class.
    """

    _access_token = None
    _access_token_expiry = None

    def __init__(self, api_key, api_secret, instance):
        """
        Initializes the HttpSession object.

        :param api_key: a Lacework API Key
        :param api_secret: a Lacework API Secret
        :param instance: a Lacework instance name

        :return HttpSession object.
        """

        super(HttpSession, self).__init__()

        # Create a requests session
        self._session = requests.Session()

        # Set the base parameters
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = f"https://{instance}.{DEFAULT_BASE_DOMAIN}"

        # Get an access token
        self._check_access_token()

    def _check_access_token(self):
        """
        A method to check the validity of the access token.
        """

        if self._access_token is None or self._access_token_expiry < datetime.now(timezone.utc):

            response = self._get_access_token()

            # Update the access token and expiration
            self._access_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=DEFAULT_ACCESS_TOKEN_EXPIRATION)
            self._access_token = response.json()["data"][0]["token"]

    def _get_access_token(self):
        """
        A method to fetch a new access token from Lacework.

        :return requests response
        """

        logger.info("Creating Access Token in Lacework...")

        uri = f"{self._base_url}/api/v1/access/tokens"

        # Build the access token request headers
        headers = {
            "X-LW-UAKS": self._api_secret,
            "Content-Type": "application/json"
        }

        # Build the access token request data
        data = {
            "keyId": self._api_key,
            "expiry_Time": DEFAULT_ACCESS_TOKEN_EXPIRATION
        }

        try:
            response = self._session.post(uri, json=data, headers=headers)

            logger.debug(response)
        except Exception:
            raise ApiError(response)

        return response

    def _get_request_headers(self):
        """
        A method to build the HTTP request headers for Lacework.
        """

        # Build the request headers
        headers = {
            "Authorization": self._access_token
        }

        return headers

    def get(self, uri):
        """
        :param uri: uri to send the HTTP GET request to
        :param headers: python object containing the header information

        :return: response json

        :raises: ApiError if unable to get a connection
        """

        self._check_access_token()

        uri = f"{self._base_url}{uri}"

        logger.info(f"GET request to URI: {uri}")

        try:
            response = self._session.get(uri, headers=self._get_request_headers())

            logger.debug(response)
        except Exception:
            raise ApiError(response)

        return response

    def post(self, uri, data=None, param=None):
        """
        :param uri: uri to send the HTTP POST request to
        :param data: json object containing the data
        :param param: python object containing the parameters

        :return: response json

        :raises: ApiError if unable to get a connection
        """

        self._check_access_token()

        uri = f"{self._base_url}{uri}"

        logger.info(f"POST request to URI: {uri}")

        try:
            response = self._session.post(uri, params=param, json=data, headers=self._get_request_headers())

            logger.debug(response)
        except Exception:
            raise ApiError(response)

        return response

    def put(self, uri, data=None, param=None):
        """
        :param uri: uri to send the HTTP POST request to
        :param data: json object containing the data
        :param param: python object containing the parameters

        :return: response json

        :raises: ApiError if unable to get a connection
        """

        self._check_access_token()

        uri = f"{self._base_url}{uri}"

        logger.info(f"PUT request to URI: {uri}")

        try:
            response = self._session.put(uri, params=param, json=data, headers=self._get_request_headers())

            logger.debug(response)
        except Exception:
            raise ApiError(response)

        return response

    def delete(self, uri):
        """
        :param uri: uri to send the http DELETE request to

        :response: reponse json

        :raises: ApiError if unable to get a connection
        """

        self._check_access_token()

        uri = f"{self._base_url}{uri}"

        logger.info(f"DELETE request to URI: {uri}")

        try:
            response = self._session.delete(uri, headers=self._get_request_headers())

            logger.debug(response)
        except Exception:
            raise ApiError(response)

        return response