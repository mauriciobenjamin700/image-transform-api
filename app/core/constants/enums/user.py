from app.core.constants.enums.base import BaseEnum


class UserRoles(str, BaseEnum):
    """
    A class to represent the user roles in the application. A user role is a representation of the role of a user in the application.

    - Attributes:
        - USER: str = "user"
        - ADMIN: str = "admin"
    """
    USER = "user"
    ADMIN = "admin"

    def __str__(self) -> str:
        return str(self.value)

    def get(self) -> str:
        return self.value


class ImageFilters(str, BaseEnum):
    """
    A class to represent the image filters in the application. An image filter is a representation of the filter applied to an image in the application.

    - Attributes:
        - GRAY: str = "gray" 
        - BLUR: str = "blur" # Aplica um desfoque à imagem.
        - DETAIL: str = "detail" # Realça os detalhes da imagem.
        - EDGE_ENHANCE: str = "edge_enhance" #  Realça as bordas da imagem.
        - EMBOSS: str = "emboss" # Aplica um efeito de relevo à imagem.
        - SHARPEN: str = "sharpen" # Aumenta a nitidez da imagem.
        - SMOOTH: str = "smooth" # Suaviza a imagem.
        
    """
    GRAY = "gray"
    BLUR = "blur"
    DETAIL = "detail"
    EDGE_ENHANCE = "edge_enhance"
    EMBOSS = "emboss"
    SHARPEN = "sharpen"
    SMOOTH = "smooth"
    
    
    def __str__(self) -> str:
        return str(self.value)

    def get(self) -> str:
        return self.value