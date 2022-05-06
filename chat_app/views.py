from django.shortcuts import render
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
import jwt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, BlacklistTokenSerializer, MessageSerializer, ParticipantSerializer
from .models import Participant, Room, Message

def get_user(access_token):
    try:
        payload = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print('payload 1 ' + str(payload))
        user = User.objects.get(id=payload['user_id'])
        print(user)
        return user
    except Exception as e:
        print(e)
        return False


def index(request):
    return render(request, 'chat_app/index.html')

def room(request, room_name):
    return render(request, 'chat_app/room.html', {
        'room_name': room_name
    })

def login(request):
    if request.method == "GET":
        return render(request, 'chat_app/login.html')
    elif request.method == "POST":
        
        print("-----------POST-----------")
        return render(request, 'chat_app/login.html')

class LoginUser(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class BlacklistToken(generics.GenericAPIView):   # For logout
    permission_classes = [AllowAny]
    serializer_class = BlacklistTokenSerializer

    def post(self, request):
        try:
            token_serializer = self.serializer_class(data=request.data)
            if token_serializer.is_valid():
                refresh_token = token_serializer.data['refresh_token']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(data={'error': token_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                'error': str(e)
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

def chatscreen(request):
    return render(request, 'chat_app/chatscreen.html')

class CreateRoom(APIView):

    def post(self, request):

        try:
            flag = 0
            access = request.data.get('access', '')
            user = get_user(access)

            # check if access token valid
            if user:
            
                receiver_id = request.data.get('receiver_id', '')
                sender_id = user.id
                # check if receiver_id is valid

                # check sender in participants
                if Participant.objects.filter(user=sender_id).exists():
                    sender_objs = Participant.objects.filter(user=sender_id)

                    for obj in sender_objs:
                        sender_room = obj.room
                        if Participant.objects.filter(user=receiver_id, room=sender_room).exists():
                            receiver_obj = Participant.objects.filter(user=receiver_id, room=sender_room)[0]
                            room = receiver_obj.room
                            # prev_messages = Message.objects.filter(room=room)
                            # ser = MessageSerializer(prev_messages, many=True)
                            return JsonResponse(data={'room_id': room.id}, safe=False, status=status.HTTP_200_OK)
                receiver_obj = User.objects.get(id=int(receiver_id))
                new_room = Room.objects.create(
                    type = '1',
                    name = f"{user.username}-{receiver_obj.username}",
                )
                Participant.objects.create(
                    user = user,
                    room = new_room
                )
                Participant.objects.create(
                    user = receiver_obj,
                    room = new_room
                )
                return JsonResponse({'room_id' : new_room.id}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChatScreen(APIView):

    def get(self, request):

        try:
            access = request.GET.get('access', '')

            user = get_user(access)
            # check if access token valid
            if user:
                # Fetch only private rooms
                user_private_room_ids = list(Participant.objects.filter(user=user, room__type='1').values_list('room', flat=True))
                participants = Participant.objects.none()
                for room in user_private_room_ids:
                    room_obj = Room.objects.get(id=int(room))
                    participants = participants | Participant.objects.filter(room=room_obj).exclude(user=user)
                ser = ParticipantSerializer(participants, many=True)

                return JsonResponse(ser.data, status=status.HTTP_200_OK, safe=False)
            
            return JsonResponse({'error' : 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewAllMessages(APIView):

    def get(self, request):
        try:
            access = request.data.get('access', '')
            user = get_user(access)
            room_obj = Room.objects.get(id=int(request.data.get('room_id', '')))

            messages = Message.objects.filter(room=room_obj)
            ser = MessageSerializer(messages, many=True)
            return JsonResponse(ser.data, status=status.HTTP_200_OK, safe=False)
        
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendMessage(APIView):

    def post(self, request):
        try:
            access = request.data.get('access', '')
            user = get_user(access)
            room_obj = Room.objects.get(id=int(request.data.get('room_id', '')))
            message = request.data.get('message', '')
            # Todo: Check if user is in room
            Message.objects.create(
                room = room_obj,
                sender = user,
                message = message,
                # Todo: Add login for sender_type
                sender_type = '0',
            )
            return JsonResponse({'message' : 'Message sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)