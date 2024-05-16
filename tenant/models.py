from django.db import models

class Tenant(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    db_user = models.CharField(max_length=100)
    db_user_password = models.CharField(max_length=100)

    def __str__(self):
        return self.id
