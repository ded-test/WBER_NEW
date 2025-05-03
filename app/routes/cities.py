from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from allcities import cities
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import *
from .auth import get_current_user

router = APIRouter()


@router.get("/cities", response_class=JSONResponse)
async def get_cities(prefix: str = ""):
    results = [
        city.name for city in cities if city.name.lower().startswith(prefix.lower())
    ]
    return {"cities": results[:5]}


@router.post("/update-city")
async def change_city(
    request: Request,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    form = await request.form()
    new_city = form.get("city")

    if not city:
        raise HTTPException(status_code=400, detail="City is required")

    result = await UserCRUD.update_city(db, user_id, new_city)

    from ..main import templates

    if result.get("status") == "success":
        return templates.TemplateResponse(
            "settings.html", {"request": request, "message": result["message"]}
        )
    else:
        raise HTTPException(status_code=400, detail=result["message"])
