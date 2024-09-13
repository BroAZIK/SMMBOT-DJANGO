from django.db import models

class media(models.Model):
    data = models.JSONField()
    user_id = models.IntegerField()        
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data: {self.data['name']},User_id: {self.user_id}"
