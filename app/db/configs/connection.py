from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.core.settings import config
from app.db.configs.base import Base
from app.db.models import *


class DBConnectionHandler:
    """
    A class to represent an database manager. It is used to manage the database connection and session.

    - Methods:
        - connect: Connect to the database.
        - disconnect: Disconnect from the database.
        - open_session: Open a new session.
        - close_session: Close the current session.
        - create_tables: Create the tables in the database.
        - drop_tables: Drop the tables in the database.
    """
    def __init__(self, db_url: str = config.DB_URL) -> None:
        self.db_url = db_url
        self.__engine = None
        self.__session_maker = None
        self.__session = None


    def connect(self):
        if self.__engine is None and self.__session_maker is None:
            self.__engine = create_engine(
                self.db_url,
                pool_pre_ping=True,
                echo=False
            )
            self.__session_maker = sessionmaker(
                self.__engine,
                expire_on_commit=False
            )
            self.__session = self.__session_maker()


    def disconnect(self):
        if self.__engine is not None and self.__session_maker is not None:
            self.__engine.dispose()
            self.__engine = None
            self.__session_maker = None
            self.__session = None

    def open_session(self):
        if self.__session is None:
            self.__session = self.__session_maker()

    def close_session(self):
        if self.__session is not None:
            self.__session.close()
            self.__session = None

    def create_tables(self):
            Base.metadata.create_all(self.__engine)

    def drop_tables(self):
            Base.metadata.drop_all(self.__engine)


    def __enter__(self):
        self.open_session()
        return self.__session

    def __exit__(self, exc_type, exc, tb):
        print(f"""
        Exception Type: {exc_type}
        Exception: {exc}
        Traceback: {tb}
        """)
        #self.close_session()
        pass


db=DBConnectionHandler(config.DB_URL)
db.connect()
