from config import settings
from sqlmodel import Session, create_engine

DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_URL}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class DatabaseSession:
    """Database session mixin."""

    def __enter__(self) -> Session:
        self.db = Session(engine)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.db.rollback()
        finally:
            self.db.close()
            # self.db.remove()


def use_database_session():
    return DatabaseSession()
