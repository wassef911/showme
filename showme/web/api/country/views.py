from fastapi import APIRouter, Depends
from typing import Annotated
from showme.services.image import ImageService
from showme.web.dependencies import ImageServiceeMarker
from starlette.responses import StreamingResponse
from showme.services.image import CountryNotFoundException
from fastapi import HTTPException

router = APIRouter()


@router.get("/country/{country_name}")
def country(
    image_service: Annotated[ImageService, Depends(ImageServiceeMarker)],
    country_name: str,
    buffer: float = 0.1,
    simplify: float = 0.01,
) -> None:
    try:
        image_buf = image_service.get_country_image(country_name, buffer, simplify)
    except CountryNotFoundException as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return StreamingResponse(
        image_buf,
        status_code=200,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=country.png"},
    )
