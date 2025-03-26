from os.path import join
from sqlalchemy.orm import Session
from PIL import Image, ImageFilter


from app.core.constants.enums.user import ImageFilters
from app.core.settings import config
from app.db.models import ImageModel
from app.db.repositories.image import ImageRepository

class ImageService:
    """
    A service class to handle image operations.
    
    - Args:
        - db_session: Session : A database session object.
        
    - Attributes:
        - repository: ImageRepository : A repository object to handle database operations for the image.
    """
    def __init__(self, db_session: Session):
        self.repository = ImageRepository(db_session)
        
    def add(self, image_id: str, filter_name: str) -> dict:
        """
        A method to add an image to the database.
        
        - Args:
            - image_id: str : The image id.
            
        - Returns:
            - image: dict : The image object.
        """
        if not image_id:
            raise ValueError("Image ID is required")
        if not filter_name:
            raise ValueError("Filter name is required")
        if filter_name not in ImageFilters.values():
            raise ValueError(f"Filter {filter_name} not found")
        
        model = ImageModel(
            name=image_id,
            url=join(config.UPLOAD_FOLDER, image_id),
            filter_applied=filter_name
        )
        image = self.repository.add(model)
        
        return image.to_dict()
        
        
    def apply_filter(self, image_id: str, filter_name: str) -> str:
        """
        A method to apply a filter to an image in the database. This method applies a filter to an image in the database.
        
        - Args:
            - image_id: str
            - filter_name: str
            
        - Returns:
            - new_image_path: str : The path of the new image.
        """
        # Abre uma imagem
        image = Image.open(join(config.UPLOAD_FOLDER, image_id))

        match filter_name:
            case ImageFilters.GRAY.value:
                new_image = image.convert('L')  # Escala de cinza
            case ImageFilters.BLUR.value:
                new_image = image.filter(ImageFilter.BLUR)
            case ImageFilters.CONTOUR.value:
                new_image = image.filter(ImageFilter.CONTOUR)
            case ImageFilters.DETAIL.value:
                new_image = image.filter(ImageFilter.DETAIL)
            case ImageFilters.EDGE_ENHANCE.value:
                new_image = image.filter(ImageFilter.EDGE_ENHANCE)
            case ImageFilters.EMBOSS.value:
                new_image = image.filter(ImageFilter.EMBOSS)
            case ImageFilters.SHARPEN.value:
                new_image = image.filter(ImageFilter.SHARPEN)
            case ImageFilters.SMOOTH.value:
                new_image = image.filter(ImageFilter.SMOOTH)
            case _:
                raise ValueError(f"Filter {filter_name} not found")
            
        new_image_path = join(config.UPLOAD_FOLDER_FILTERED, image_id)
            
        new_image.save(new_image_path)

        return new_image_path