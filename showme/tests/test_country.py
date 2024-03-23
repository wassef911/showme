import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_getting_country_image(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    url = "api/country/tunisia"
    response = await client.get(
        url,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "image/png"
    assert response.headers["content-disposition"] == "attachment; filename=country.png"


@pytest.mark.anyio
async def test_getting_country_image_exc_not_found(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    url = "api/country/wassef"
    response = await client.get(
        url,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
