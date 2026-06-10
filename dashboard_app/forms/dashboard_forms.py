from django import forms
from dashboard_app.models import dashboard_models

class SupportForm(forms.ModelForm):
    class Meta:
        model = dashboard_models.Support
        fields = ['name', 'enlisted_email', 'contact_no', 'business_name', 'problem_statement', 'attachment']
        labels = {
            'enlisted_email': "Enlisted Email",
            'contact_no': "Contact Number",
            'business_name': "Business Name",
            'problem_statement': "Problem Statement",
            'attachment': "Attachment",
        }
        widgets = {
            'problem_statement': forms.Textarea(attrs={'rows':'3', 'cols':'3'})
        }