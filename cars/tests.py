
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Car


User = get_user_model()


class CarAPITests(APITestCase):

    def setUp(self):
        self.car = Car.objects.create(
            brand="Toyota",
            model="Prius",
            year=2022,
            price="12000.00",
        )

    def test_car_list(self):
        response = self.client.get("/api/cars/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_register(self):
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "email": "new@example.com",
            "password": "StrongPass123!",
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertIn("token", response.data)
        self.assertTrue(
            Token.objects.filter(user__username="newuser").exists()
        )

    def test_login(self):
        User.objects.create_user(
            username="testuser",
            password="StrongPass123!",
        )

        response = self.client.post("/api/login/", {
            "username": "testuser",
            "password": "StrongPass123!",
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_admin_can_create_car(self):
        admin = User.objects.create_user(
            username="adminuser",
            password="StrongPass123!",
            is_staff=True,
        )

        token = Token.objects.create(user=admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.post("/api/cars/", {
            "brand": "BMW",
            "model": "X5",
            "year": 2023,
            "price": "25000.00",
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_normal_user_cannot_create_car(self):
        user = User.objects.create_user(
            username="normaluser",
            password="StrongPass123!",
        )

        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.post("/api/cars/", {
            "brand": "BMW",
            "model": "X5",
            "year": 2023,
            "price": "25000.00",
        })

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
