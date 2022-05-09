from random import choices
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):

    ROOM_TYPE = (
        ('0', 'Public'),
        ('1', 'Private'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(choices=ROOM_TYPE, max_length=1, help_text="Public- 0, Private- 1")

    def __str__(self):
        return self.name
    
class Participant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} | {self.room.name}"

class Message(models.Model):

    SENDER_TYPE = (
        ('0', 'Job Seeker'),
        ('1', 'School District'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_type = models.CharField(choices=SENDER_TYPE, max_length=1, help_text="Job Seeker- 0, School District- 1")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender.username} | {self.room.name}"