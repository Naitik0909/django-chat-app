from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from urllib.parse import parse_qs
import urllib.parse
import jwt


# def get_user(user_id):
#     try:
#         return User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return AnonymousUser()

@database_sync_to_async
def get_user(access_token):
    try:
        payload = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print('payload 1 ' + str(payload))
        user = User.objects.get(id=payload['user_id'])
        print(user)
        return user
    except Exception as e:
        print(e)
        return AnonymousUser()

class CustomAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        # Parse query_string
        query_params = parse_qs(scope["query_string"].decode())
        print("HEY", query_params)
        scope['user'] = await get_user(query_params['access'][0])
        # scope['user'] = await get_user(int(scope["query_string"]))

        return await self.app(scope, receive, send)
