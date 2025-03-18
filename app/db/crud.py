from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.future import select
from app.db.models import DataUser, DataEvent
from datetime import datetime, time
from typing import Union

class UserCRUD:
    @staticmethod
    async def create_user(db: AsyncSession, username: str, mail: str,
                          city: str, password: bytes, salt: bytes):
        try:
            user = DataUser(
                username=username,
                mail=mail,
                city=city,
                password=password,
                salt=salt
            )
            db.add(user)
            await db.commit()
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}
        except Exception as e:
            await db.rollback()
            return {"error": f"Unexpected error: {str(e)}"}

    @staticmethod
    async def get_user(db: AsyncSession, identifier: Union[str, int]):

        if isinstance(identifier, int) or identifier.isdigit():
            identifier = int(identifier)
            search_criteria = {"id": identifier}
        else:
            search_criteria = {"mail": identifier}

        result = await db.execute(select(DataUser).filter_by(**search_criteria))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_mail(db: AsyncSession, identifier: int):
        user = await UserCRUD.get_user(db, identifier)
        return user.mail if user else None

    @staticmethod
    async def get_city(db: AsyncSession, identifier: int):
        user = await UserCRUD.get_user(db, identifier)
        return user.city if user else None

    @staticmethod
    async def check_username(db: AsyncSession, username: str) -> bool:
        result = await db.execute(select(DataUser).filter(DataUser.username == username))
        return result.scalar() is not None

    @staticmethod
    async def check_mail(db: AsyncSession, mail: str) -> bool:
        result = await db.execute(select(DataUser).filter(DataUser.mail == mail))
        return result.scalar() is not None

    @staticmethod
    async def update_city(db: AsyncSession, user_id: int, new_city: str):
        try:
            user = await UserCRUD.get_user(db, user_id)
            if not user:
                return {"error": "User not found"}
            if user.city == new_city:
                return {"message": "City is already set to this value"}

            user.city = new_city
            await db.commit()
            return {"message": f"City updated to {new_city}"}
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}


class EventCRUD:
    @staticmethod
    async def create_event(db: AsyncSession, user_id: int, event_date: datetime, name: str,
                           description: str, category: bool):
        try:
            event = DataEvent(
                user_id=user_id,
                event_date=event_date,
                name=name,
                description=description,
                category=category
            )
            db.add(event)
            await db.commit()
            await db.refresh(event)
            return event
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}

    @staticmethod
    async def update_event(db: AsyncSession, event_id: int, user_id: int, event_date: datetime,
                           name: str, description: str, category: bool):
        try:
            result = await db.execute(select(DataEvent).filter_by(id=event_id, user_id=user_id))
            event = result.scalars().first()

            if not event:
                return {"error": "Event not found"}

            if event_date is not None:
                event.event_date = event_date
            if name is not None:
                event.name = name
            if description is not None:
                event.description = description
            if category is not None:
                event.category = category

            await db.commit()
            await db.refresh(event)
            return {"message": "Event updated successfully"}

        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}

    @staticmethod
    async def delete_event(db: AsyncSession, event_id: int, user_id: int):
        try:
            result = await db.execute(select(DataEvent).filter_by(id=event_id, user_id=user_id))
            event = result.scalars().first()

            if not event:
                return {"error": "Event not found"}

            deleted_event = {"id": event.id, "name": event.name}

            await db.delete(event)
            await db.commit()

            return {"message": "Event deleted successfully", "deleted_event": deleted_event}

        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}

    @staticmethod
    async def get_event(db: AsyncSession, user_id: int, event_date: datetime):
        try:
            start_of_day = datetime.combine(event_date, time.min)
            end_of_day = datetime.combine(event_date, time.max)

            events = await db.execute(
                select(DataEvent).where(
                    DataEvent.user_id == user_id,
                    DataEvent.event_date >= start_of_day,
                    DataEvent.event_date <= end_of_day
                )
            )
            events = events.scalars().all()
            return events

        except SQLAlchemyError as e:
            return {"error": f"Database error: {str(e)}"}
