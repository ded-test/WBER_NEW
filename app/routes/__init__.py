from .auth import router as auth_router
from .cities import router as cities_router
from .users import router as users_router
from .events import router as events_router
from .weather import router as weather_router

__all__ = [
    "auth_router",
    "cities_router",
    "users_router",
    "events_router",
    "weather_router",
]
