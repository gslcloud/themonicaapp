from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError, IntegrityError
from contextlib import contextmanager
from app.models.waving_models import Waver
from app.database import db_path

engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class WavingManager:
    def update_waving_data(self, username: str) -> bool:
        with get_session() as session:
            waver = session.query(Waver).filter_by(username=username).first()

            if waver:
                waver.waving_count += 1
            else:
                waver = Waver(username=username, waving_count=1)
                session.add(waver)

            try:
                session.commit()
                return True
            except (DatabaseError, IntegrityError):
                session.rollback()
                return False

    def get_recent_wavers(self):
        with get_session() as session:
            recent_wavers = session.query(Waver.username).order_by(Waver.id.desc()).limit(5).all()
            return [waver[0] for waver in recent_wavers]


def get_waving_manager():
    return WavingManager()
