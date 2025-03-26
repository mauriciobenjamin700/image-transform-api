import pytest

from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND
from app.core.errors import NotFoundError
from app.schemas.user import UserRequest, UserResponse
from app.services.user import UserService


def test_user_service_get_success(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)
    response_db = service.add(request)

    # Act

    response = service.get_by_id(response_db.id)

    # Assert

    assert isinstance(response, UserResponse)
    assert response == response_db


def test_user_service_get_fail_not_found(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)

    service.add(request)

    # Act

    with pytest.raises(NotFoundError) as e:
        service.get_by_id("123")

    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_USER_NOT_FOUND
