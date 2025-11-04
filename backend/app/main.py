"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .config import get_settings
from .database import engine
from .models import init_db


settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.add_middleware(
        CORSMiddleware,
        #allow_origins=settings.cors_allowed_origins,
        allow_origins=settings.get_cors_origins_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db(engine)

    @app.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    return app


app = create_application()
