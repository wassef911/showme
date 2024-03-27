from fastapi import APIRouter, Depends
from typing import Annotated
from showme.services.image import ImageService
from showme.web.dependencies import ImageServiceeMarker
from starlette.responses import StreamingResponse, Response
from showme.services.image import CountryNotFoundException
from pydantic import BaseModel
from fastapi import HTTPException
from showme.tkq import run_coutries_by_name, run_coutries_by_eco, run_coutries_by_income
from starlette import status

router = APIRouter()


class StringList(BaseModel):
    filter_values: list[str]


@router.get("/country_name/{country_name}")
def get_country_by_name(
    image_service: Annotated[ImageService, Depends(ImageServiceeMarker)],
    country_name: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> StreamingResponse:
    formatted_country_name = country_name.lower().capitalize()
    try:
        image_buf = image_service.get_country_image(
            "sovereignt",
            formatted_country_name,
            buffer,
            simplify,
        )
    except CountryNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return StreamingResponse(
        image_buf,
        status_code=status.HTTP_200_OK,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=country.png"},
    )


@router.get("/economy/{economy}")
def get_countries_by_economy(
    image_service: Annotated[ImageService, Depends(ImageServiceeMarker)],
    economy: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> StreamingResponse:
    try:
        image_buf = image_service.get_country_image(
            "economy",
            economy,
            buffer,
            simplify,
        )
    except CountryNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return StreamingResponse(
        image_buf,
        status_code=status.HTTP_200_OK,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=country.png"},
    )


@router.get("/income/{group}")
def get_countries_by_income(
    image_service: Annotated[ImageService, Depends(ImageServiceeMarker)],
    group: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> StreamingResponse:
    try:
        image_buf = image_service.get_country_image(
            "income_grp",
            group,
            buffer,
            simplify,
        )
    except CountryNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return StreamingResponse(
        image_buf,
        status_code=status.HTTP_200_OK,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=country.png"},
    )


@router.post("/batch/{filter_by}")
async def post_batch(
    image_service: Annotated[ImageService, Depends(ImageServiceeMarker)],
    filter_by: str,
    filter_values: StringList,
) -> Response:
    if filter_by == "country_name":
        for filter_value in filter_values:
            await run_coutries_by_name.kiq(filter_value)
    elif filter_by == "economy":
        for filter_value in filter_values:
            await run_coutries_by_eco.kiq(filter_value)
    elif filter_by == "group":
        for filter_value in filter_values:
            await run_coutries_by_income.kiq(filter_value)
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid filter_by value, must be one of: country_name, economy, group",
        )
    return Response(status_code=status.HTTP_201_CREATED)
