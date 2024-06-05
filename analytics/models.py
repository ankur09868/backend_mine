from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class CLTV(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    cltv_value = models.DecimalField(max_digits=10, decimal_places=2)
