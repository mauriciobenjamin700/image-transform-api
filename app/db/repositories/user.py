from sqlalchemy import (
    delete,
    select
)
from sqlalchemy.orm import Session

from app.core.constants.messages import (
    ERROR_DATABASE_USER_ALREADY_EXISTS,
    ERROR_DATABASE_USER_NOT_FOUND,
    ERROR_REQUIRED_FIELD_ID
)
from app.core.errors import (
    ConflictError,
    NotFoundError,
    ValidationError
)
from app.db.models import UserModel


class UserRepository:
    """
    User Repository Class to handle all database operations related to User

    - Attributes:
        - db_session: Session

    - Methods:
        - add: Add a new User to the database
        - get: Get a User from the database
        - update: Update a User in the database
        - delete: Delete a User from the database
    """
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session


    def add(self, model: UserModel) -> UserModel:
        """
        Add a new User to the database

        - Args:
            - model: UserModel

        - Returns:
            - UserModel
        """

        try:
            self.db_session.add(model)
            self.db_session.commit()
            self.db_session.refresh(model)
            return model

        except Exception as e:
            print("USER REPOSITORY ADD ERROR: ",e)
            self.db_session.rollback()
            raise ConflictError(ERROR_DATABASE_USER_ALREADY_EXISTS)


    def get(self, id: str = None, email: str = None, all_results = False) -> None | UserModel | list[UserModel]:
        """
        Get a User from the database by id or email. If all_results is True, return all results found in the database.

        - Args:
            - id: str = None
            - email: str = None
            - all_results: bool = False

        - Returns:
            - UserModel
            - List[UserModel]
        """
        if id:
            stmt = select(UserModel).where(UserModel.id == id)
        elif email:
            stmt = select(UserModel).where(UserModel.email == email)
        else:
            stmt = select(UserModel)

        result = self.db_session.execute(stmt)

        if all_results:
            return result.scalars().all()

        return result.scalars().first()


    def update(self, model: UserModel) -> UserModel:
        """
        Update a User in the database

        - Args:
            - model: UserModel

        - Returns:
            - UserModel
        """
        self.db_session.commit()
        self.db_session.refresh(model)
        return model


    def delete(self, model: UserModel = None, id: str = None) -> None:
        """
        Delete a User from the database. If model is provided, delete the model. If id is provided, delete the model with the id.

        - Args:
            - model: UserModel : User model to delete
            - id: str : Id of the User model to delete

        - Returns:
            - None
        """
        if model:
            self.db_session.delete(model)
            self.db_session.commit()
        elif id:
            stmt = delete(UserModel).where(UserModel.id == id)
            result = self.db_session.execute(stmt)
            self.db_session.commit()

            if result.rowcount == 0:
                raise NotFoundError(ERROR_DATABASE_USER_NOT_FOUND)

        else:
            raise ValidationError("id",ERROR_REQUIRED_FIELD_ID)
