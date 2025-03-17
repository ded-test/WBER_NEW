from fastapi import APIRouter

router = APIRouter()


# @app.get("/settings")
# async def read_settings(
#     request: Request, current_user: str = Depends(get_current_user)
# ):
#     city = await get_user_city(current_user)
#     if not city:
#         raise HTTPException(status_code=404, detail="User's city not found.")
#     return templates.TemplateResponse(
#         "settings.html", {"request": request, "city": city}
#     )


