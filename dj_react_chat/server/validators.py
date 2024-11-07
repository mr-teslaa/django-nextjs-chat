import os
from PIL import Image
from django.core.exceptions import ValidationError


def validate_icon_image_size(image: Image) -> None:
    """
    Validate the size of an icon image.

    Args:
        image: The image to validate.

    Raises:
        ValidationError: If the image size is larger than 70x70.
    """
    if not image:
        return

    with Image.open(image) as img:
        if img.width > 70 or img.height > 70:
            raise ValidationError("Image size should be equal or less than 70x70")


def validate_image_file_extension(image):
    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png"]

    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension.")
