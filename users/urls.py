from rest_framework.routers import DefaultRouter, SimpleRouter

from users.viewsets import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)


urlpatterns = router.urls
