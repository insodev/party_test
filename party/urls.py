from rest_framework.routers import DefaultRouter

from . import views

app_name = 'party-api'

router = DefaultRouter()
router.register(r'party', views.PartyViewSet, basename='party')

urlpatterns = router.urls
