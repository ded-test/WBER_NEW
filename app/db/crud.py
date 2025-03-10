from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import DataUser
from sqlalchemy.exc import SQLAlchemyError

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, mail: str, city: str, password: bytes, salt: bytes):
        try:
            user = DataUser(
                username=username,
                mail=mail,
                city=city,
                password=password,
                salt=salt
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"error": f"Database error: {str(e)}"}

    def get_user(self, user_id: int):
        user = self.db.query(DataUser).filter(DataUser.id == user_id).first()
        if not user:
            return {"error": "User not found"}
        return user

    def get_mail(self, user_id: int):
        user = self.get_user(user_id)
        return user.mail if user else None

    def get_city(self, user_id: int):
        user = self.get_user(user_id)
        return user.city if user else None

    def update_city(self, user_id: int, new_city: str):
        try:
            user = self.get_user(user_id)
            if not user:
                return {"error": "User not found"}
            if user.city == new_city:
                return {"message": "City is already set to this value"}

            user.city = new_city
            self.db.commit()
            return {"message": f"City updated to {new_city}"}
        except SQLAlchemyError as e:
            self.db.rollback()
            return {"error": f"Database error: {str(e)}"}


class EventCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, user_id: int, event_date: str, name: str, description: str, category: ):
        try:


    def update_event(self):

    def delete_event(self):

    def get_event(self):
