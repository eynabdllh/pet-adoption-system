from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.email