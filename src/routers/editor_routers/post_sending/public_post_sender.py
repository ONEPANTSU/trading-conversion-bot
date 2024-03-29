from src.routers.editor_routers.post_sending.post_sender import PostSender


class PublicPostSender(PostSender):
    async def _get_users(self, language_code: str):
        return await self.user_service.get_users_by_language(language_code)
