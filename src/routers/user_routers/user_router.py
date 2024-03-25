from aiogram import Router

from src.services.user_service import UserService


class UserRouter(Router):
    def __init__(self, user_service: UserService):
        super().__init__(name="user-router")
        self.user_service = user_service
