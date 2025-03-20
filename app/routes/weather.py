from fastapi import APIRouter, Request, Depends, HTTPException
import httpx
from ..core.config import settings
from ..db import UserCRUD
from ..routes.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()

@router.get("/weather")
async def get_weather(
    request: Request,
    date: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):

    city = await UserCRUD.get_city(db,user_id)

    if not city:
        raise HTTPException(status_code=404, detail="User's city not found.")

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.API_KEY_WEATHER}&units=metric&lang=en"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Ошибка получения данных о погоде.",
                )
            data = response.json()

            forecast_for_date = [
                entry for entry in data["list"] if entry["dt_txt"].split(" ")[0] == date
            ]

            if not forecast_for_date:
                return {"message": f"Нет данных о погоде для {city} на {date}."}

            forecast_str = "\n".join(
                [
                    f"{entry['dt_txt'].split(' ')[1][:5]}      {entry['main']['temp']}°C, {entry['weather'][0]['description']} {get_weather_emoji(entry['weather'][0]['description'])}"
                    for entry in forecast_for_date
                ]
            )

            return {"city": data["city"]["name"], "forecast": forecast_str.split("\n")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_weather_emoji(description: str) -> str:
    description = description.lower()
    if "clear" in description or "ясно" in description:
        return "☀️"
    elif "cloud" in description or "облачно" in description:
        return "☁️"
    elif "rain" in description or "дождь" in description:
        return "🌧️"
    elif "snow" in description or "снег" in description:
        return "❄️"
    elif "thunderstorm" in description or "гроза" in description:
        return "⚡"
    elif "drizzle" in description or "морось" in description:
        return "🌦️"
    elif "fog" in description or "туман" in description:
        return "🌫️"
    else:
        return "🌍"
