from lexloop.repositories.word_repository import WordModel


def ensure_tables() -> None:
    if not WordModel.exists():
        WordModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
