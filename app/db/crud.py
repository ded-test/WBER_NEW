from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.db.models import DataUser, DataEvent
from datetime import date, time
from typing import Union


class UserCRUD:
    @staticmethod
    async def create_user(
        db: AsyncSession,
        username: str,
        mail: str,
        city: str,
        password: bytes,
        salt: bytes,
    ):
        try:
            user = DataUser(
                username=username, mail=mail, city=city, password=password, salt=salt
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
        if isinstance(identifier, int) or (
            isinstance(identifier, str) and identifier.isdigit()
        ):
            identifier = int(identifier)
            search_filter = DataUser.id == identifier
        else:
            search_filter = DataUser.mail == identifier

        result = await db.execute(select(DataUser).filter(search_filter))
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
        result = await db.execute(
            select(DataUser).filter(DataUser.username == username)
        )
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
                return {"status": "success"}

            user.city = new_city
            await db.commit()
            await db.refresh(user)
            return {"message": f"City updated to {new_city}"}
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error: {str(e)}"}


class EventCRUD:
    @staticmethod
    async def create_event(
        db: AsyncSession,
        user_id: int,
        event_date: date,
        event_time: time,
        name: str,
        description: str,
        category: bool,
    ):
        try:
            event = DataEvent(
                user_id=user_id,
                event_date=event_date,
                event_time=event_time,
                name=name,
                description=description,
                category=category,
            )
            db.add(event)
            await db.commit()
            await db.refresh(event)
            return event
        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error in create_event: {str(e)}"}

    @staticmethod
    async def update_event(
        db: AsyncSession,
        event_id: int,
        user_id: int,
        event_date: date,
        event_time: time,
        name: str,
        description: str,
        category: bool,
    ):
        try:
            result = await db.execute(
                select(DataEvent).filter_by(id=event_id, user_id=user_id)
            )
            event = result.scalars().first()

            if not event:
                return {"error": "Event not found"}

            if event_date is not None:
                event.event_date = event_date
            if event_time is not None:
                event.event_time = event_time
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
            return {"error": f"Database error in update_event: {str(e)}"}

    @staticmethod
    async def delete_event(db: AsyncSession, event_id: int, user_id: int):
        try:
            result = await db.execute(
                select(DataEvent).filter_by(id=event_id, user_id=user_id)
            )
            event = result.scalars().first()

            if not event:
                return {"error": "Event not found"}

            deleted_event = {"id": event.id, "name": event.name}

            await db.delete(event)
            await db.commit()

            return {
                "message": "Event deleted successfully",
                "deleted_event": deleted_event,
            }

        except SQLAlchemyError as e:
            await db.rollback()
            return {"error": f"Database error in delete_event: {str(e)}"}

    @staticmethod
    async def get_event(db: AsyncSession, user_id: int, event_date: date):
        try:
            events = await db.execute(
                select(DataEvent)
                .where(DataEvent.user_id == user_id, DataEvent.event_date == event_date)
                .order_by(DataEvent.event_time)
            )
            events = events.scalars().all()
            return events

        except SQLAlchemyError as e:
            return {"error": f"Database error in get_event: {str(e)}"}

    @staticmethod
    async def get_event_id(db: AsyncSession, event_id: int):
        try:
            result = await db.execute(select(DataEvent).where(DataEvent.id == event_id))
            event = result.scalar_one_or_none()
            return event
        except SQLAlchemyError as e:
            return {"error": f"Database error in get_event_id: {str(e)}"}
