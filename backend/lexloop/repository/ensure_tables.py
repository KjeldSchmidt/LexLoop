from lexloop.auth.user_repository import UserRepo
from lexloop.repository.link_repository import LinkRepo
from lexloop.repository.node_repository import NodeRepo
from lexloop.repository.tag_repository import TagRepo


def ensure_tables() -> None:
    if not NodeRepo.exists():
        NodeRepo.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
    if not LinkRepo.exists():
        LinkRepo.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

    if not TagRepo.exists():
        TagRepo.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )

    if not UserRepo.exists():
        UserRepo.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
