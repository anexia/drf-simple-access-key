from copy import deepcopy

from django.conf import settings
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase


class SimpleAuthorizationKeyAPITestCase(APITestCase):
    @staticmethod
    def get_rest_framework_test_settings(
        authorization_key, authorization_header=None, authorization_scheme=None
    ):
        """
        Create a deep copy of the `SIMPLE_ACCESS_KEY_SETTINGS` settings and replace the `AUTHORIZATION_KEYS` for testing in
        override_settings
        """
        rest_framework_test_settings = deepcopy(settings.SIMPLE_ACCESS_KEY_SETTINGS)
        rest_framework_test_settings["AUTHORIZATION_KEYS"] = authorization_key

        if authorization_header:
            rest_framework_test_settings[
                "HTTP_AUTHORIZATION_HEADER"
            ] = authorization_header

        if authorization_scheme:
            rest_framework_test_settings[
                "HTTP_AUTHORIZATION_SCHEME"
            ] = authorization_scheme

        return rest_framework_test_settings

    def test_empty_authorization_keys(self):
        data = {}
        url = reverse("book-list")

        # Check with empty string
        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings("")
        ):
            response = self.client.get(url, data, format="json")
            self.assertEqual(response.status_code, 200)

            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="12345678"
            )
            self.assertEqual(response.status_code, 200)

            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 12345678"
            )
            self.assertEqual(response.status_code, 200)

        # Check with None
        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(None)
        ):
            response = self.client.get(url, data, format="json")
            self.assertEqual(response.status_code, 200)

            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="12345678"
            )
            self.assertEqual(response.status_code, 200)

            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 12345678"
            )
            self.assertEqual(response.status_code, 200)

    def test_simple_authorization_keys(self):
        data = {}
        url = reverse("book-list")

        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(
                ["12345678"]
            )
        ):
            response = self.client.get(url, data, format="json")
            self.assertEqual(response.status_code, 403)

            # no bearer, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="12345678"
            )
            self.assertEqual(response.status_code, 403)

            # bearer only, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with first letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 1"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with second letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 2"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with middle parts of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 34"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with last letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 8"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with invalid token based on correct token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 123456789"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with invalid token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 25423523"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with valid token, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 12345678"
            )
            self.assertEqual(response.status_code, 200)

            # mixed case bearer with valid token, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="BeaReR 12345678"
            )
            self.assertEqual(response.status_code, 200)

    def test_multiple_authorization_keys(self):
        data = {}
        url = reverse("book-list")

        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(
                ["123", "345", "678"]
            )
        ):
            response = self.client.get(url, data, format="json")
            self.assertEqual(response.status_code, 403)

            # no bearer, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="123"
            )
            self.assertEqual(response.status_code, 403)

            # bearer only, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with first letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 1"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with second letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 2"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with middle parts of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 34"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with last letter of the token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 8"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with invalid token based on correct token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 1234"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with invalid token, should fail
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 234234"
            )
            self.assertEqual(response.status_code, 403)

            # bearer with valid token 1, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 123"
            )
            self.assertEqual(response.status_code, 200)

            # bearer with valid token 2, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 345"
            )
            self.assertEqual(response.status_code, 200)

            # bearer with valid token 3, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer 678"
            )
            self.assertEqual(response.status_code, 200)

            # mixed case bearer with valid token 1, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="BeaReR 123"
            )
            self.assertEqual(response.status_code, 200)

            # mixed case bearer with valid token 2, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="BeaReR 345"
            )
            self.assertEqual(response.status_code, 200)

            # mixed case bearer with valid token 3, should work
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="BeaReR 678"
            )
            self.assertEqual(response.status_code, 200)

    def test_symbols_authorization_keys(self):
        data = {}
        url = reverse("book-list")

        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(
                '|`F:#vj$9~[M<{qTt4}AXq"Ncd'
            )
        ):
            # bearer with valid token, should work
            response = self.client.get(
                url,
                data,
                format="json",
                HTTP_X_AUTHORIZATION='bearer |`F:#vj$9~[M<{qTt4}AXq"Ncd',
            )
            self.assertEqual(response.status_code, 200)

            # mixed case bearer with valid token, should work
            response = self.client.get(
                url,
                data,
                format="json",
                HTTP_X_AUTHORIZATION='BeaReR |`F:#vj$9~[M<{qTt4}AXq"Ncd',
            )
            self.assertEqual(response.status_code, 200)

    def test_custom_authorization_header(self):
        data = {}
        url = reverse("book-list")

        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(
                "key1", authorization_header="auth"
            )
        ):
            # invalid header
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer key1"
            )
            self.assertEqual(response.status_code, 403)

            # valid header
            response = self.client.get(
                url, data, format="json", HTTP_AUTH="BeaReR key1"
            )
            self.assertEqual(response.status_code, 200)

    def test_custom_authorization_scheme(self):
        data = {}
        url = reverse("book-list")

        with override_settings(
            SIMPLE_ACCESS_KEY_SETTINGS=self.get_rest_framework_test_settings(
                "key1", authorization_scheme="test"
            )
        ):
            # invalid header
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="bearer key1"
            )
            self.assertEqual(response.status_code, 403)

            # valid header
            response = self.client.get(
                url, data, format="json", HTTP_X_AUTHORIZATION="test key1"
            )
            self.assertEqual(response.status_code, 200)
