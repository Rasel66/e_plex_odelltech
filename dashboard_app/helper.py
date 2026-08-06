import requests
from django.conf import settings
def get_support_details(support_id):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    response = requests.get(
        f"{settings.SUPPORT_DETAIL_API}{support_id}/",
        headers=headers
    )

    return response
def reply_support_ticket(ticket_id, data, files=None):

    headers = {
        "X-API-KEY": settings.SUPPORT_API_KEY
    }

    response = requests.post(
        f"{settings.SUPPORT_REPLY_API}{ticket_id}/reply/",
        headers=headers,
        data=data,
        files=files
    )

    return response