from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    contact_no = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email