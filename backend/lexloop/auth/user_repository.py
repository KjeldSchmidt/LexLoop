from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from lexloop.repository.base import Base


class UserRepo(SQLAlchemyBaseUserTableUUID, Base):
    pass
