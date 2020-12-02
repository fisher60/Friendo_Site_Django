import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


class User(AbstractUser):
    """Custom user class, contains django backend as well as discord data for users."""

    bot_admin = models.BooleanField(default=False)
    discord_id = models.BigIntegerField(
        blank=True, null=True, default=None, unique=True
    )
    discord_username = models.CharField(
        max_length=100, blank=True, null=True, default=None
    )
    discord_discriminator = models.CharField(
        max_length=4, blank=True, null=True, default=None
    )
    discord_avatar = models.CharField(
        max_length=100, blank=True, null=True, default=None
    )
    is_bot = models.BooleanField(blank=True, default=False)

    @property
    def notes(self):
        return [x.content for x in self.note_set.all()]

    def clear_tokens(self):
        """
        Delete all existing AuthTokens the user has.
        :return: None
        """
        auth_tokens = self.authtoken_set.all()
        # if user has existing tokens, delete them all
        if auth_tokens:
            for token in auth_tokens:
                token.delete()

    def generate_token(self):
        """
        creates a new token for the current user
        :return: AuthToken
        """
        auth_token = AuthToken(user=self)
        auth_token.set_expiration()
        auth_token.encode_token()

        # clear previous tokens before saving
        self.clear_tokens()

        auth_token.save()

        return auth_token


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} || {self.id}"


class Currency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=97)

    def __str__(self):
        return "Chad Bucks"


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
    def __str__(self):
        return f"{self.user.username} || {self.token[-5:-1]}"

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
        ).decode("utf-8")
        self.token = encode_token

    def validate_token(self):
        """
        Validates whether this token is valid based on expiration time and current time
        :return: True if token is valid else false
        """
        return datetime.now() < self.expiration


def validate_token(token: str) -> bool:
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    try:
        expiration_time = payload["exp"]
        if datetime.now() < datetime.fromtimestamp(expiration_time):
            return True
        else:
            raise PermissionDenied("Token expired")
    except KeyError:
        raise PermissionDenied("Token could not be validated.")


def token_auth(info):
    """
    Attempts to get an authorization token from the request headers,
    then authenticates the request if the token is valid and belongs to a user.

    :param info: all of the information from the request/args[1]
    :return: True if token is valid else False or raise the appropriate error
    """

    context = info.context.get("request", None)
    if context:
        headers = context.headers

        try:
            authorization = headers["Authorization"]
        except KeyError:
            raise PermissionDenied("Authorization not provided.")

        authorization = authorization.split()

        # check auth type
        if authorization[0] == "Bearer":

            # check that there are two args, auth type and token
            if len(authorization) == 2:
                token = authorization[1]

                # check if token is valid
                token_confirm = validate_token(token)

                # token exists
                if token_confirm:
                    return True
                else:
                    raise PermissionDenied("Invalid Token")

            # Too few or too many args in Authorization
            else:
                raise ValueError("Auth type or Token missing/invalid")

        # Authorization was not not "Bearer"
        else:
            raise ValueError("Invalid Auth type")

    return False


def token_required(func):
    """
    Decorator wrapper to require token authentication for a specific request.

    :param func: the original function that invoked this decorator.
    :return: the orginal function with args and kwargs if the token was authorized, else raise permission error
    """

    def inner(*args, **kwargs):
        _, info, *__ = args

        # Request and token valid
        if token_auth(info):
            return func(*args, **kwargs)

        # Invalid request, authorization, or token
        else:
            raise PermissionDenied("Token Auth Failed")

    return inner
