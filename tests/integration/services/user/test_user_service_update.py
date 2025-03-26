import pytest

from app.core.constants.messages import ERROR_DATABASE_USER_NOT_FOUND
from app.core.errors import NotFoundError
from app.core.security.password import verify_password
from app.schemas.user import UserRequest, UserResponse
from app.services.user import UserService


def test_user_service_update_success(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)
    response_db = service.add(request)
    update = UserRequest(**request.to_dict())
    update.name = "New Name"
    update.email = "new@email.com"
    update.phone = "889123456789"
    update.password = "newPassword@"


    # Act

    response = service.update(response_db.id, update)
    model = service.repository.get(id=response_db.id)
    # Assert

    assert isinstance(response, UserResponse)
    assert response.name == update.name.upper()
    assert response.email == update.email
    assert response.phone == update.phone
    assert verify_password(update.password, model.password)


def test_user_service_update_fail_not_found(mock_db_session, mock_user_request):

    # Arrange

    service = UserService(mock_db_session)
    request = UserRequest(**mock_user_request)

    service.add(request)

    # Act

    with pytest.raises(NotFoundError) as e:
        service.update("123", request)

    # Assert

    assert e.value.status_code == 404
    assert e.value.detail == ERROR_DATABASE_USER_NOT_FOUND
