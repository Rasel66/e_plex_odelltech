from django.db import models
from dashboard_app.models import choices
from accounts.models import phone_number_validator, User

class Support(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_user', blank=True, null=True)
    name = models.CharField(max_length=100)
    enlisted_email = models.EmailField()
    contact_no = models.CharField(max_length=20, validators=[phone_number_validator])
    business_name = models.CharField(max_length=250, blank=True, null=True)
    problem_statement = models.TextField()
    attachment = models.FileField(upload_to='support_attachment/', blank=True, null=True)
    status = models.CharField(max_length=20,choices=choices.SUPPORT_STATUS_CHOICE, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
