from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Paginator:
    key: str = 'pagination'
    items: list = []
    prev_btn: str = 'prev'
    next_btn: str = 'next'
    current_page: int = 0

    router: Router

    def __init__(self, **attrs) -> None:
        self.__dict__.update(**attrs)

        self._declare_handler()

    async def _pagination_handler(self, query: CallbackQuery) -> None:
        (request, page) = query.data.split(':')

        self.current_page = int(page)

        if query.message.caption:
            await query.message.edit_caption(
                caption=self.get_current_page(),
                reply_markup=self.get_keyboard().as_markup(),
                disable_web_page_preview=True,
            )
        else:
            await query.message.edit_text(
                text=self.get_current_page(), reply_markup=self.get_keyboard().as_markup(), disable_web_page_preview=True
            )

    def _declare_handler(self):
        self.router.callback_query.register(
            self._pagination_handler,
            F.data.startswith(self.key)
        )

    def get_keyboard(self) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()

        if len(self.items) > 0:

            if self.current_page > 0:
                builder.button(text=self.prev_btn, callback_data=f"{self.key}:{self.current_page -1}")

            if self.current_page < len(self.items) - 1:
                builder.button(text=self.next_btn, callback_data=f"{self.key}:{self.current_page +1}")

        return builder

    def get_current_page(self) -> str:
        return self.items[self.current_page]
