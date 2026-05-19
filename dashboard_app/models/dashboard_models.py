from django.db import models
from dashboard_app.models import choices
from accounts.models import phone_number_validator, User

class Support(models.Model):
    support_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_user', blank=True, null=True)
    name = models.CharField(max_length=100)
    enlisted_email = models.EmailField()
    contact_no = models.CharField(max_length=20, validators=[phone_number_validator])
    business_name = models.CharField(max_length=250, blank=True, null=True)
    problem_statement = models.TextField()
    attachment = models.FileField(upload_to='support_attachment/', blank=True, null=True)
    status = models.CharField(max_length=20,choices=choices.SUPPORT_STATUS_CHOICE, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.support_id:
            last_support = Support.objects.order_by('-id').first()
            if last_support and last_support.support_id:
                last_number = int(last_support.support_id.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.support_id = f'SUP-{new_number:04d}'
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class GetItNow(models.Model):
    full_name = models.CharField(max_length=200)
    contact_no = models.CharField(max_length=20, validators=[phone_number_validator])
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    contacted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='get_it_now_contacted', blank=True, null=True)
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name