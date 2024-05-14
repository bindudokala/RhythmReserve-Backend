from django.db import models

class ChatSession(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    session_start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.session_start}"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=100)  # guest / username

    def __str__(self):
        return f"{self.sender} - {self.created_at}: {self.text}"


