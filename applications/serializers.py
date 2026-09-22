from rest_framework import serializers

from .models import DeveloperApplication, Membership


class DeveloperApplicationSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
    )

    class Meta:
        model = DeveloperApplication
        fields = [  # noqa: RUF012
            "id",
            "organization",
            "organization_name",
            "created_by_username",
            "name",
            "description",
            "callback_url",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [  # noqa: RUF012
            "id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate_organization(self, organization):
        request = self.context["request"]

        allowed_roles = [Membership.Role.ADMIN, Membership.Role.DEVELOPER]

        has_permission = Membership.objects.filter(
            organization=organization, user=request.user, role_in=allowed_roles
        ).exists()
        
        if not has_permission:
            raise serializers.ValidationError(
                "You must be an admin or developer in this organization."
            )
            
        return organization
