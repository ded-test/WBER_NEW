from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..routes.auth import get_current_user
from ..db import *
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/settings")
async def read_settings(
    request: Request,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    city = await UserCRUD.get_city(db, user_id)

    from ..main import templates

    if not city:
        raise HTTPException(status_code=404, detail="User's city not found.")
    return templates.TemplateResponse(
        "settings.html", {"request": request, "city": city}
    )

@router.post("/update_city")
async def change_city(
        request: Request,
        user_id: str = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
        ):

    form = await request.form()
    city = form.get("city")

    if not city:
        raise HTTPException(status_code=404, detail="User's city not found.")

    new_city = await UserCRUD.update_city(db, user_id, city)

    from ..main import templates

    if new_city["status"] == "success":
        return templates.TemplateResponse("settings.html", {"request": request})
    else:
        return templates.TemplateResponse(
            "settings.html", {"request": request, "error": new_city["message"]}
        )

@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response