from django.contrib.auth import authenticate, get_user_model

from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Car
from .serializers import CarSerializer, RegisterSerializer
from .permissions import IsAdminOrReadOnly


User = get_user_model()


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by("-id")
    serializer_class = CarSerializer
    permission_classes = [IsAdminOrReadOnly]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        request=request,
        username=username,
        password=password,
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "username": user.username,
            "token": token.key,
        },
        status=status.HTTP_200_OK,
    )
