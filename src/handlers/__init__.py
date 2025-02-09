from aiogram import Router

from handlers.message import router as message_router

router = Router()
router.include_routers(
    message_router,
)

__all__ = [
    "router",
]
