from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Query
from app.db.session import get_db
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_current_user
from ..db.crud import EventCRUD

router = APIRouter()


@router.get("/get_events")
async def get_events(
    request: Request,
    event_date: str = Query(),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        event_date = datetime.strptime(event_date, "%Y-%m-%d")
        events = await EventCRUD.get_event(
            db=db, user_id=int(user_id), event_date=event_date
        )
        event_list = [
            {
                "id": event.id,
                "user_id": event.user_id,
                "name": event.name,
                "description": event.description,
                "category": event.category,
                "event_date": event.event_date,
                "event_time": event.event_time,
            }
            for event in events
        ]
        return {"events": events}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event: {str(e)}")


@router.post("/create_event")
async def create_event(
    request: Request,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    form = await request.form()
    event_date_str = form.get("event_date")
    event_time = form.get("event_time")
    name = form.get("name")
    description = form.get("description")
    category_str = form.get("category")
    category = True if category_str.lower() == "true" else False

    print(event_date_str, event_time, name, description, category_str)

    if not all([event_date_str, name, description]):
        raise HTTPException(status_code=400, detail="All fields are required")

    try:
        if isinstance(event_date_str, datetime):
            event_date = event_date_str.date()
        elif isinstance(event_date_str, str):
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    try:
        event_time = datetime.strptime(event_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат времени")

    try:
        event = await EventCRUD.create_event(
            db=db,
            user_id=int(user_id),
            event_date=event_date,
            event_time=event_time,
            name=name,
            description=description,
            category=bool(category),
        )
        return {"message": "Event create successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register event: {str(e)}"
        )


@router.post("/update_event")
async def update_event(
    request: Request,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    form = await request.form()
    event_id = form.get("event_id")
    event_date_str = form.get("event_date")
    event_time_str = form.get("event_time")
    name = form.get("name")
    description = form.get("description")
    category_str = form.get("category")

    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")

    if not event_date_str:
        raise HTTPException(status_code=400, detail="Event date is required")

    try:
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    if len(event_time_str) == 8:
        event_time = datetime.strptime(event_time_str, "%H:%M:%S").time()
    else:
        event_time = datetime.strptime(event_time_str + ":00", "%H:%M:%S").time()

    try:
        event = await EventCRUD.update_event(
            db=db,
            event_id=int(event_id),
            user_id=int(user_id),
            event_date=event_date,
            event_time=event_time,
            name=name,
            description=description,
            category=category_str.lower() == "true",
        )
        return {"message": "Event update successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update event: {str(e)}")


@router.get("/get_event_for_update/{event_id}")
async def get_event_for_update(event_id: int, db: AsyncSession = Depends(get_db)):
    try:
        event = await EventCRUD.get_event_id(db=db, event_id=event_id)
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event: {str(e)}")


@router.delete("/delete_event")
async def delete_event(
    request: Request,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    form = await request.form()
    event_id = form.get("event_id")

    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")

    try:
        await EventCRUD.delete_event(
            db=db, event_id=int(event_id), user_id=int(user_id)
        )
        return {"message": "Event deleted successfully", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")
