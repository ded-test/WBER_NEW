from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from models import DataUser, DataEvent
from datetime import datetime, time

class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, mail: str,
                          city: str, password: bytes, salt: bytes):
        try:
            user = DataUser(
                username=username,
                mail=mail,
                city=city,
                password=password,
                salt=salt
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

    async def get_user(self, user_id: int):
        result = await self.db.execute(select(DataUser).filter(DataUser.id == user_id))
        return result.scalar()

    async def get_mail(self, user_id: int):
        user = await self.get_user(user_id)
        return user.mail if user else None

    async def get_city(self, user_id: int):
        user = await self.get_user(user_id)
        return user.city if user else None

    async def check_username(self, username: str):
        result = await self.db.execute(select(DataUser).filter(DataUser.username == username))
        return result.scalar() is None

    async def check_mail(self, mail: str):
        result = await self.db.execute(select(DataUser).filter(DataUser.mail == mail))
        return result.scalar() is None

    async def update_city(self, user_id: int, new_city: str):
        try:
            user = await self.get_user(user_id)
            if not user:
                return {"error": "User not found"}
            if user.city == new_city:
                return {"message": "City is already set to this value"}

            user.city = new_city
            await self.db.commit()
            return {"message": f"City updated to {new_city}"}
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

class EventCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, user_id: int, event_date: datetime, name: str,
                           description: str, category: bool):
        try:
            event = DataEvent(
                user_id=user_id,
                event_date=event_date,
                name=name,
                description=description,
                category=category
            )
            self.db.add(event)
            await self.db.commit()
            await self.db.refresh(event)
            return event
        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

    async def update_event(self, event_id: int, user_id: int, event_date: datetime,
                           name: str, description: str, category: bool):
        try:
            result = await self.db.execute(select(DataEvent).filter_by(id=event_id, user_id=user_id))
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

            await self.db.commit()
            await self.db.refresh(event)
            return {"message": "Event updated successfully"}

        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

    async def delete_event(self, event_id: int, user_id: int):
        try:
            result = await self.db.execute(select(DataEvent).filter_by(id=event_id, user_id=user_id))
            event = result.scalars().first()

            if not event:
                return {"error": "Event not found"}

            deleted_event = {"id": event.id, "name": event.name}

            await self.db.delete(event)
            await self.db.commit()

            return {"message": "Event deleted successfully", "deleted_event": deleted_event}

        except SQLAlchemyError as e:
            await self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

    async def get_event(self, user_id: int, event_date: datetime):
        try:
            # Ограничим поиск события по дате
            start_of_day = datetime.combine(event_date, time.min)
            end_of_day = datetime.combine(event_date, time.max)

            events = await self.db.execute(
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
