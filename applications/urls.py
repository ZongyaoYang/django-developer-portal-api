from rest_framework.routers import DefaultRouter

from .views import DeveloperApplicationViewSet

router = DefaultRouter()
router.register(
    "applications", DeveloperApplicationViewSet, basename="developer-application"
)

urlpattern = router.urls
