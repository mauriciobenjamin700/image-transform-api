from pytest import fixture

from app.core.constants.enums.user import UserRoles
from app.core.security.password import hash_password
from app.core.settings import config
from app.db.configs.connection import DBConnectionHandler


@fixture
def mock_db_session():
    test_db = DBConnectionHandler(config.TEST_DB_URL)
    test_db.connect()
    test_db.create_tables()
    
    with test_db as session:

        yield session

    test_db.drop_tables()



@fixture
def mock_user_request():
    return {
        "name": "John Doe",
        "phone": "(89) 91111-2222",
        "email": "jhon.doe@gmail.com",
        "password" : "SafePassword123@"
    }


@fixture
def mock_user_model():
    return {
        "name": "John Doe",
        "phone": "(89) 91111-2222",
        "email": "jhon.doe@gmail.com",
        "password" : hash_password("SafePassword123@"),
        "role": UserRoles.USER.value
    }
