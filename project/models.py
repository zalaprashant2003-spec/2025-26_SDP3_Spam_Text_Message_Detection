from django.db import models

# Create your models here.
class EmailAccount(models.Model):
    email = models.EmailField(unique=True)      # Stores the email
    password = models.CharField(max_length=255) # Stores the password

    def __str__(self):
        return self.email
