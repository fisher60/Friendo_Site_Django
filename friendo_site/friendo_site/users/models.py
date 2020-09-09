import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest


class User(AbstractUser):
    bot_admin = models.BooleanField(default=False)


class Token(models.Model):
    """Abstract token model"""

    expiration = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=4096)

    class Meta:
        abstract = True

    @staticmethod
    def get_expiration():
        """
        Calculate the expiration time
        """
        raise NotImplementedError()

    def encode_token(self):
        """
        abstract method override
        """
        raise NotImplementedError()


class AuthToken(Token):
    @staticmethod
    def get_expiration() -> datetime:
        """Calculate the expiration time for Auth Token"""
        token_delta = settings.JWT_AUTH_TOKEN_DELTA
        if not isinstance(token_delta, timedelta):
            raise ImproperlyConfigured(
                "JWT_AUTH_TOKEN_DELTA must be an instance of datetime.timedelta."
            )
        return datetime.now() + token_delta

    def set_expiration(self):
        self.expiration = self.get_expiration()

    def encode_token(self):
        """Encode a user Authentication token."""
        if not self.expiration:
            raise ValueError("set the token expiration before encoding.")
        if not self.user or not isinstance(self.user, User):
            raise ValueError("set the token user before encoding")

        encode_time = datetime.utcnow()
        payload = {
            "exp": self.expiration,
            "nbf": encode_time,
            "iat": encode_time,
            "user": self.user.username,
            "is_admin": self.user.is_superuser,
        }
        encode_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        self.token = encode_token


def token_required(func):
    def inner(*args, **kwargs):
        _, info, *__ = args
        context = info.context.get("request", None)
        if context:
            headers = context.headers
            try:
                authorization = headers["Authorization"]
            except KeyError:
                raise ValueError("Authorization not provided.")
            authorization = authorization.split()
            if authorization[0] == "Bearer":
                if len(authorization) == 2:
                    token = authorization[1]
                else:
                    raise ValueError("Auth type or Token missing")
            else:
                raise ValueError("Invalid Auth type")
        return func(*args, **kwargs)

    return inner
