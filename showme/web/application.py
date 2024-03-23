from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from showme.services.image import ImageService
from showme.web.dependencies import ImageServiceeMarker
from showme.log import configure_logging
from showme.web.api.router import api_router
from showme.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="showme",
        version="1.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    image_service = ImageService()

    def get_image_service() -> ImageService:
        return image_service

    app.dependency_overrides.update(
        {
            ImageServiceeMarker: get_image_service,
        },
    )
    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
