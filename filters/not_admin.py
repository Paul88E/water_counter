from aiogram.types import Message
from aiogram.filters import BaseFilter


class NotAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id not in self.admin_ids
