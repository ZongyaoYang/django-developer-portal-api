import uuid

from django.conf import settings
from django.db import models

# Create your models here.

# Create 3 tables:
# User ──< Membership >── Organization ──< DeveloperApplication


# A user can belong to multiple organizations.
# An organization can have multiple users.
# Membership stores the user’s role within an organization.
# Each developer application belongs to exactly one organization.
class Organization(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]  # noqa: RUF012

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        DEVELOPER = "developer", "Developer"
        VIEWER = "viewer", "Viewer"

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.DEVELOPER)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["organization", "user"],
                name="unique_organization_memberships",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.organization.name} ({self.role})"


class DeveloperApplication(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="developer_applications",
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    callback_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # noqa: RUF012
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_application_name_per_organization",
            )
        ]

        indexes = [  # noqa: RUF012
            models.Index(
                fields=["organization", "status"],
                name="app_org_status_idx",
            )
        ]

    def __str__(self) -> str:
        return f"{self.organization.name} - {self.name}"
