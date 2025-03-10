from .auth import router as auth_router
from .events import router as events_router
from .users import router as users_router
from .weather import router as weather_router

__all__ = ["auth_router","events_router","users_router","weather_router"]
