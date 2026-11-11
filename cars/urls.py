from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CarViewSet, RegisterView, login_view


router = DefaultRouter()
router.register("cars", CarViewSet, basename="car")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
] + router.urls
