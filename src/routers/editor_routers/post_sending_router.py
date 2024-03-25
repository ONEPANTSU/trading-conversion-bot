from src.routers.editor_routers.abstract_post_sending_router import (
    AbstractPostSendingRouter,
)
from src.routers.editor_routers.post_sending.post_sender import PostSender
from src.routers.utils.callbacks.editor_callback_data import (
    CHOOSE_MAILING_LANGUAGE_DATA,
    SUBMIT_SEND_MAILING_MESSAGE_DATA,
)
from src.routers.utils.states.editor_states.send_post_state import (
    SendPostState,
)
from src.services.editor_service import EditorService
from src.services.user_service import UserService


class PostSendingRouter(AbstractPostSendingRouter):
    def __init__(
        self,
        editor_service: EditorService,
        user_service: UserService,
    ):
        super().__init__(
            editor_service,
            user_service,
            name="post-sending-router",
            send_post_button="send-post",
            choose_lang_callback_data=CHOOSE_MAILING_LANGUAGE_DATA,
            submit_send_callback_data=SUBMIT_SEND_MAILING_MESSAGE_DATA,
            state=SendPostState,
            post_sender=PostSender,
        )
