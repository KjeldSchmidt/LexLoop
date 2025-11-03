from sqlalchemy.orm import declarative_base


from lexloop.auth.user_repository import UserRepo
from lexloop.repository.link_repository import LinkRepo
from lexloop.repository.node_repository import NodeRepo
from lexloop.repository.tag_repository import TagRepo

Base = declarative_base()
__all__ = ["UserRepo", "LinkRepo", "NodeRepo", "TagRepo"]
