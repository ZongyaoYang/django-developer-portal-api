from typing import cast

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from .models import DeveloperApplication
from .serializers import DeveloperApplicationSerializer


# Create your views here.
class DeveloperApplicationViewSet(ModelViewSet):
    serializer_class = DeveloperApplicationSerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]  # noqa: RUF012

    def get_queryset(self):
        request = cast(Request, self.request)
        queryset = (
            DeveloperApplication.objects.filter(
                organization__memberships__user=self.request.user
            )
            .select_related("organization", "created_by")
            .distinct()
        )
        
        status_value = request.query_params.get("status")
        
        if status_value:
            queryset = queryset.filter(status=status_value)
            
        return queryset
