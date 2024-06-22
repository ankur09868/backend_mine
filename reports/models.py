from django.db import models

class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    leads_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_leads = models.IntegerField(default=0)

    def __str__(self):
        return f"Report {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
