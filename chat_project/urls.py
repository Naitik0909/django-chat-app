
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.conf import settings

from chat_app.views import LoginUser, BlacklistToken, chatscreen, ChatScreen, CreateRoom, ViewAllMessages, SendMessage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat_app.urls')),
    # path('register/', RegisterUser.as_view(),name="register"),
    path('logout/blacklist/', BlacklistToken.as_view(),name="blacklist"),
    path('login/', LoginUser.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', chatscreen, name='chat_screen'),
    path('create_room/', CreateRoom.as_view(), name='create_room'),
    path('chat_screen/', ChatScreen.as_view(), name='get_all_chats'),
    path('view_messages/', ViewAllMessages.as_view(), name='view_messages'),
    path('send_message/', SendMessage.as_view(), name='send_message'),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)