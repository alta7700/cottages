from PIL import Image

from django.db.models.fields.files import ImageFieldFile
from django.core.exceptions import ValidationError

__all__ = ["validate_16x9_jpeg"]


def validate_16x9_jpeg(image: ImageFieldFile):
    pil_img = Image.open(image.file)
    if pil_img.format != 'JPEG':
        raise ValidationError('Фотография должна быть формата jpeg/jpg')
    if pil_img.width / pil_img.height != 16 / 9:
        raise ValidationError(
            'Соотношения сторон фотографии должны быть 16/9 '
            f'(1280×720, 1920×1080, 2560×1440, 3840×2160, ...). Разрешение на фото {pil_img.width}×{pil_img.height}'
        )
