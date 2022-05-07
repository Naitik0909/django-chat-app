from os import sendfile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import Message, Participant, Room

from datetime import datetime, timedelta

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        # user_type = None
        # user = self.user
        # if JobSeeker.objects.filter(user = user).exists():
        #     user_type = 'JobSeeker'
        # elif DistrictAdmin.objects.filter(user=user).exists() or DistrictNonAdmin.objects.filter(user=user).exists():
        #     user_type = 'DistrictAdmin'
        # data['user'] = user_type
        return data
    default_error_messages = {
        'no_active_account': _('Please enter correct credentials.')
    }

class BlacklistTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)

    def validate(self, attrs):
        if len(attrs['refresh_token']) < 10:
            raise serializers.ValidationError({"refresh_token": 'Token too short'})

        return attrs

class MessageSerializer(serializers.ModelSerializer):

    sender_name     = serializers.SerializerMethodField('get_sender_name')
    sent_at_time    = serializers.SerializerMethodField('get_sent_at_time')
    sent_at_date    = serializers.SerializerMethodField('get_sent_at_date')
    # room_name = serializers.SerializerMethodField('get_room_name')
    # room_type = serializers.SerializerMethodField('get_room_type')

    class Meta:
        model = Message
        fields = ('id', 'sender','sender_name','message', 'sender_type', 'sent_at_time', 'sent_at_date')
    
    def get_sender_name(self, obj):
        sender = obj.sender
        return f"{sender.first_name} {sender.last_name}"
    
    def get_sent_at_time(self, obj):
        return obj.sent_at.strftime("%I:%M %p")

    def get_sent_at_date(self, obj):
        today = datetime.today()
        if obj.sent_at.date() == today.date():
            return "Today"
        elif obj.sent_at.date() == today.date() - timedelta(days=1):
            return "Yesterday"
        else:
            return obj.sent_at.strftime("%d %B")
    # def get_room_name(self, obj):
    #     room = obj.room
    #     return f"{room.name}"

    # def get_room_type(self, obj):
    #     room = obj.room
    #     return f"{room.type}"

class ParticipantSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField('get_user_name')

    class Meta:
        model = Participant
        fields = ('room', 'user', 'user_name')

    def get_user_name(self, obj):
        user = obj.user
        return f"{user.first_name} {user.last_name}"