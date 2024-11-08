from fastapi import FastAPI
from uvicorn import run

from duroveswall.config import DefaultSettings, get_settings
from duroveswall.routes import list_of_routes


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """

    application = FastAPI(
        title="Du Rove's Wall",
    )
    settings = get_settings()
    bind_routes(application, settings)
    return application


app = get_app()

if __name__ == "__main__":
    settings_for_application = get_settings()
    run(
        "duroveswall.__main__:app",
        host=settings_for_application.APP_ADDRESS,
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["duroveswall", "tests"],
        log_level="debug",
    )