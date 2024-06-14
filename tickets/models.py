from django.db import models
from accounts.models import Account
from contacts.models import Contact

class Ticket(models.Model):
    CASE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    TYPE_CHOICES = [
        ('issue', 'Issue'),
        ('request', 'Request'),
        ('bug', 'Bug'),
    ]
    CASE_ORIGIN_CHOICES = [
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('web', 'Web'),
        ('social_media', 'Social Media'),
    ]

    casenumber = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    webemail = models.EmailField(max_length=254)
    case_reason = models.CharField(max_length=200) 
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES)
    date = models.DateField()
    owner = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, related_name='Ticket', on_delete=models.CASCADE, blank=True, null=True)
    account = models.ForeignKey(Account, related_name='Ticket', on_delete=models.CASCADE, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES) 
    case_origin = models.CharField(max_length=20, choices=CASE_ORIGIN_CHOICES)

    def __str__(self):
        return f"Ticket {self.casenumber}: {self.subject}"