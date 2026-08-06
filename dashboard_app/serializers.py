from rest_framework import serializers
from dashboard_app.models import dashboard_models


class SupportCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = dashboard_models.Support
        fields = (
            "name",
            "enlisted_email",
            "contact_no",
            "business_name",
            "problem_statement",
            "attachment",
        )



class SupportListSerializer(serializers.ModelSerializer):
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = dashboard_models.Support
        fields = (
            "support_id",
            "name",
            "enlisted_email",
            "contact_no",
            "business_name",
            "problem_statement",
            "attachment",
            "status",
            "remarks",
        )

    def get_attachment(self, obj):
        request = self.context.get("request")

        if obj.attachment:
            if request:
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url

        return None



class SupportReplySerializer(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%d %b %Y, %I:%M %p",
        read_only=True
    )

    class Meta:
        model = dashboard_models.SupportReply

        fields = (
            "id",
            "sender",
            "message",
            "attachment",
            "is_central_reply",
            "created_at",
        )

    def get_sender(self, obj):

        if obj.user:
            return obj.user

        return "Support Team"


class SupportDetailSerializer(serializers.ModelSerializer):

    replies = SupportReplySerializer(many=True, read_only=True)

    class Meta:
        model = dashboard_models.Support

        fields = (
            "support_id",
            "name",
            "enlisted_email",
            "contact_no",
            "business_name",
            "problem_statement",
            "attachment",
            "status",
            "remarks",
            "replies",
        )

SUPPORT_STATUS_CHOICE = (
    ('', "--SELECT--"),
    ('pending', "Pending"),
    ('on_progress', "On Progress"),
    ('solved', "Solved")
)



class AdminSupportReplySerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(
        choices=SUPPORT_STATUS_CHOICE,
        write_only=True
    )

    class Meta:
        model = dashboard_models.SupportReply
        fields = (
            "message",
            "attachment",
            "status",
        )