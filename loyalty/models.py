from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from tenant.models import Tenant 
from contacts.models import Contact


class Loyalty(models.Model):
    LOYALTY_PROGRAMS = (
        ('Promo Code', 'Promo Code'),
        ('Loyalty Cards', 'Loyalty Cards'),
        ('Fidelity Cards', 'Fidelity Cards'),
        ('Promotional Program', 'Promotional Program'),
        ('Coupons', 'Coupons'),
        ('2+1 Free', '2+1 Free'),
        ('Next Order Coupons' , 'Next Order Coupons')
    )
    CURRENCY_CHOICES = (
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('JPY', 'Japanese Yen'),
    ('INR', 'Indian Rupee'),
)

    entity_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    entity = GenericForeignKey('content_type' , 'entity_id')
    
    loyalty_program = models.CharField(max_length=50, choices=LOYALTY_PROGRAMS)
    contacts = models.ForeignKey(Contact, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    points_unit = models.IntegerField(default=0),
    start_date = models.DateField(),
    end_date = models.DateField(),
    company = models.CharField(max_length=50),
    website = models.URLField(blank=True, null=True)

    
    def __str__(self):
        return f'{self.loyalty_program} with {self.entity}'
