from django.db import models

class ValentineDay(models.Model):
    title = models.CharField(max_length=100)  # e.g., "Rose Day"
    date_to_unlock = models.DateField()       # e.g., 2026-02-07
    
    # The Lock
    clue_question = models.CharField(max_length=255) # e.g., "Where did we first meet?"
    correct_answer = models.CharField(max_length=100) # e.g., "cubbon park"
    
    # The Reward (Unlocked Content)
    love_letter = models.TextField()
    photo = models.ImageField(upload_to='memories/', blank=True, null=True) # Her photos
    music = models.FileField(upload_to='music/', blank=True, null=True)     # Your songs (CTRL+HEART)
    
    def __str__(self):
        return self.title