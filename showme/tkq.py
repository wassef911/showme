import taskiq_fastapi
from taskiq import InMemoryBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from showme.services.image import ImageService, CountryNotFoundException
from showme.services.blob import ImageStorageService
from loguru import logger

from showme.settings import settings

result_backend = RedisAsyncResultBackend(
    redis_url=str(settings.redis_url.with_path("/1")),
)
broker = ListQueueBroker(
    str(settings.redis_url.with_path("/1")),
).with_result_backend(result_backend)

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "showme.web.application:get_app",
)

# Singletons
image_service = ImageService()
storage_service = ImageStorageService(
    settings.azure_blob_connection_string,
    settings.azure_blob_container_name,
)


@broker.task
async def run_coutries_by_name(
    countries_names: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> list[str]:
    """
    Task to get countries by name.
    Returns the links of images created.
    """
    image_urls = []
    for i, country_name in enumerate(countries_names):
        formatted_country_name = country_name.lower().capitalize()
        filter_name = "sovereignt"
        blob_name = f"{filter_name}_{formatted_country_name}.png"
        try:
            buff = image_service.get_country_image(
                filter_name,
                formatted_country_name,
                buffer,
                simplify,
            )
        except CountryNotFoundException as exc:
            logger.error(f"Error processing country {country_name}: {exc}")
            continue
        storage_service.upload_image_if_not_exists(blob_name, buff)
        image_urls.append(storage_service.get_image_url(blob_name))

    logger.info(f"Processed {image_urls} countries")
    return image_urls


@broker.task
async def run_coutries_by_eco(
    economies: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> list[str]:
    """
    Task to get countries by economy.
    Returns the links of images created.
    """
    image_urls = []
    for i, economy in enumerate(economies):
        filter_name = "economy"
        blob_name = f"{filter_name}_{economy}.png"
        try:
            buff = image_service.get_country_image(
                filter_name,
                economy,
                buffer,
                simplify,
            )
        except CountryNotFoundException as exc:
            logger.error(f"Error processing country {economy}: {exc}")
            continue
        storage_service.upload_image_if_not_exists(blob_name, buff)
        image_urls.append(storage_service.get_image_url(blob_name))
    return image_urls


@broker.task
async def run_coutries_by_income(
    income_grps: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> list[str]:
    """
    Task to get countries by group name.
    Returns the links of images created.
    """
    image_urls = []
    for i, income_grp in enumerate(income_grps):
        filter_name = "economy"
        blob_name = f"{filter_name}_{income_grp}.png"
        try:
            buff = image_service.get_country_image(
                filter_name,
                income_grp,
                buffer,
                simplify,
            )
        except CountryNotFoundException as exc:
            logger.error(f"Error processing country {income_grp}: {exc}")
            continue
        storage_service.upload_image_if_not_exists(blob_name, buff)
        image_urls.append(storage_service.get_image_url(blob_name))
    return image_urls
