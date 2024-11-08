from duroveswall.routes.auth import api_router as auth_router
from duroveswall.routes.entry import api_router as entry_router


list_of_routes = [
    auth_router,
    entry_router,
]


__all__ = [
    "list_of_routes",
]
