from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication


class SimpleAccessKeyAuthentication(BaseAuthentication):
    """
    This is an authentication that is assigned to endpoint for OpenAPI generation when using the
    SimpleAccessKey permission.

    The authentication returns an AnonymousUser, as the checks are done in the permission class.
    """

    def authenticate(self, request):
        return AnonymousUser(), None


try:
    from drf_spectacular.extensions import OpenApiAuthenticationExtension
    from drf_spectacular.plumbing import build_bearer_security_scheme_object

    class SimpleAccessKeyAuthenticationScheme(OpenApiAuthenticationExtension):
        target_class = (
            "drf_simple_access_key.authentication.SimpleAccessKeyAuthentication"
        )
        name = "SimpleAccessKey"

        def get_security_definition(self, auto_schema):
            return build_bearer_security_scheme_object(
                header_name=settings.SIMPLE_ACCESS_KEY_SETTINGS[
                    "HTTP_AUTHORIZATION_HEADER"
                ],
                token_prefix=settings.SIMPLE_ACCESS_KEY_SETTINGS[
                    "HTTP_AUTHORIZATION_SCHEME"
                ],
            )

except ImportError:
    pass
