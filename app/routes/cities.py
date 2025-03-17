from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from allcities import cities
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
async def changing_city(request: Request, current_user: str = Depends(get_current_user)):
    form = await request.form()
    city = form.get("city")

    if not city:
        raise HTTPException(status_code=400, detail="City is required")

    print(f"Received city: {city}")

    current_user = int(current_user)

    result = await UserCRUD.update_city(user_id=current_user, new_city=city)

    from ..main import templates

    if result.get("status") == "success":
        return templates.TemplateResponse(
            "settings.html", {"request": request, "message": result["message"]}
        )
    else:
        raise HTTPException(status_code=400, detail=result["message"])
