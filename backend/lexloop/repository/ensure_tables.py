from lexloop.repository.word_repository import WordRepo


def ensure_tables() -> None:
    if not WordRepo.exists():
        WordRepo.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )
