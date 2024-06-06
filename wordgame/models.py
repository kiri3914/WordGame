from django.db import models
from authorization.models import CustomerUser

class Word(models.Model):
    word = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.word

class Game(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    win = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username} - {self.word}"

class Attempt(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    guessed_word = models.CharField(max_length=5)
    attempts = models.IntegerField(default=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.guessed_word} ({self.attempts})"


