from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from models import DataUser

class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, mail: str, city: str, password: bytes, salt: bytes):
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



# class EventCRUD:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def create_event(self):
#
#     def update_event(self):
#
#     def delete_event(self):
#
#     def get_event(self):
