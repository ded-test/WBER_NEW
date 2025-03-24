from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Query
from app.db.session import get_db
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_current_user
from ..db.crud import EventCRUD

router = APIRouter()

@router.get("/get_events")
async def get_events(request: Request,
                    event_date: datetime = Query(),
                    user_id: int = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    try:
        events = await EventCRUD.get_event(
            db=db,
            user_id=user_id,
            event_date=event_date
        )
        return {"events": events}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get event: {str(e)}"
        )

@router.post("/update_event")
async def update_event(request: Request,
                       event_date: datetime = Query(),
                       user_id: int = Depends(get_current_user)):

    form = await request.form()
    event_id = form.get("event_id")
    name = form.get("name")
    description = form.get("description")
    category = form.get("category")

    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")

    try:
        event = await EventCRUD.update_event(
            event_id=event_id,
            user_id=user_id,
            event_date=event_date,
            name=name,
            description=description,
            category=category
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update event: {str(e)}")

    return {"event": event}

@router.post("/create_event")
async def create_event(request: Request,
                       user_id: int = Depends(get_current_user),
                       event_date: datetime = Query()):

    form = await request.form()
    name = form.get("name")
    description = form.get("description")
    category = form.get("category")

    if not all([event_date, name, description, category]):
        raise HTTPException(status_code=400, detail="All fields are required")

    try:
        event = await EventCRUD.create_event(
            user_id=user_id,
            event_date=event_date,
            name=name,
            description=description,
            category=category
        )
        return {"event": event}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register event: {str(e)}")

@router.delete("/delete_event")
async def delete_event(request: Request,
                       user_id: int = Depends(get_current_user)):

    form = await request.form()
    event_id = form.get("event_id")

    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")

    try:
        await EventCRUD.delete_event(
            event_id=event_id,
            user_id=user_id
        )
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")


