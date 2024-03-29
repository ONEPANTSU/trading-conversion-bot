from src.routers.editor_routers.abstract_post_sending_router import (
    AbstractPostSendingRouter,
)
from src.routers.editor_routers.post_sending.private_post_sender import (
    PrivatePostSender,
)
from src.routers.utils.callbacks.editor_callback_data import (
    CHOOSE_PRIVATE_MAILING_LANGUAGE_DATA,
    SUBMIT_SEND_PRIVATE_MAILING_MESSAGE_DATA,
)
from src.routers.utils.states.editor_states.send_private_post_state import (
    SendPrivatePostState,
)
from src.services.users.editor_service import EditorService
from src.services.users.user_service import UserService


class PrivatePostSendingRouter(AbstractPostSendingRouter):
    def __init__(
        self,
        editor_service: EditorService,
        user_service: UserService,
    ):
        super().__init__(
            editor_service,
            user_service,
            name="private-post-sending-router",
            send_post_button="send-private-post",
            choose_lang_callback_data=CHOOSE_PRIVATE_MAILING_LANGUAGE_DATA,
            submit_send_callback_data=SUBMIT_SEND_PRIVATE_MAILING_MESSAGE_DATA,
            state=SendPrivatePostState,
            post_sender=PrivatePostSender,
        )
