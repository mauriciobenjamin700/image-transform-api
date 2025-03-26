from sqlalchemy.orm import Session

from app.db.models import ImageModel

class ImageRepository:
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
        
    def add(self, image: ImageModel) -> ImageModel:
        """
        A method to add an image to the database. This method adds an image to the database.
        
        - Args:
            - image: ImageModel
            
        - Returns:
            - ImageModel: The image model added to the database.
        """
        self.db_session.add(image)
        self.db_session.commit()
        self.db_session.refresh(image)
        
        return image
    
    def get(self, image_id: str = None) -> ImageModel | None:
        """
        A method to get an image from the database. This method gets an image from the database.
        
        - Args:
            - image_id: str
            
        - Returns:
            - ImageModel: The image model from the database.
        """
        if not image_id:
            return self.db_session.query(ImageModel).all()
        return self.db_session.query(ImageModel).filter(ImageModel.id == image_id).first()
    
    
    def delete(self, image_id: str) -> ImageModel:
        """
        A method to delete an image from the database. This method deletes an image from the database.
        
        - Args:
            - image_id: str
            
        - Returns:
            - ImageModel: The image model deleted from the database.
        """
        self.db_session.query(ImageModel).filter(ImageModel.id == image_id).delete()
        self.db_session.commit()
        
    