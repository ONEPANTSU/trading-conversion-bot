from src.routers.editor_routers.post_sending.post_sender import PostSender


class PrivatePostSender(PostSender):

    async def __get_users(self, language_code: str):
        return await self.user_service.get_users_with_privacy_by_language(language_code)
