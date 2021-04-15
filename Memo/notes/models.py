from django.db import models

class Note(models.Model):
    content = models.CharField(max_length=200, default="Digita sua anotação!")
    
    def __str__(self):
        return (f"{self.content}")