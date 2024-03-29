from src.routers.admin_routers.admin_settings_router import AdminSettingsRouter
from src.routers.admin_routers.editor_settings_router import (
    EditorSettingsRouter,
)
from src.routers.common_routers.command_router import CommandRouter
from src.routers.common_routers.language_router import LanguageRouter
from src.routers.editor_routers.get_media_id_router import GetMediaIDRouter
from src.routers.editor_routers.post_sending_router import PostSendingRouter
from src.routers.editor_routers.private_post_sending_router import (
    PrivatePostSendingRouter,
)
from src.routers.user_routers.user_register_router import UserRegisterRouter
from src.services.service_registry import ServiceRegistry


class RouterRegistry:

    def __init__(self, services: ServiceRegistry):
        self.command_router = CommandRouter(
            services.admin_service,
            services.editor_service,
            services.user_service,
        )
        self.admin_settings_router = AdminSettingsRouter(
            services.admin_service
        )
        self.editor_settings_router = EditorSettingsRouter(
            services.editor_service, services.admin_service
        )
        self.post_sending_router = PostSendingRouter(
            services.editor_service, services.user_service
        )
        self.private_post_sending_router = PrivatePostSendingRouter(
            services.editor_service, services.user_service
        )
        self.get_media_id_router = GetMediaIDRouter(services.editor_service)
        self.user_register_router = UserRegisterRouter(
            services.user_service, services.parsing_service
        )
        self.language_router = LanguageRouter(services.user_service)

    def get_list(self):
        return [
            self.__dict__[router]
            for router in self.__dict__
            if router.endswith("_router")
        ]
