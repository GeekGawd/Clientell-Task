from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Opportunity(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='opportunities')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')

    def __str__(self) -> str:
        return f"{self.account.name} --> {self.amount}"