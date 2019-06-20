"""Factories to create a working user and related models."""
from django.contrib.auth import get_user_model


class UserDetailsFactory():
    def __init__(self):
        user = self.create_user()

        self.user = user

    def create_user(self):
        UserModel = get_user_model()
        user = UserModel.objects.create()

        return user
