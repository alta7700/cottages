from io import BytesIO

from PIL import Image


def make_progressive_jpeg(image):
    with Image.open(image) as img:
        file = BytesIO()
        img.save(file, "JPEG", quality=80, optimize=True, progressive=True)
        return file


def is_progressive_jpeg(image):
    with Image.open(image) as img:
        return img.info.get('progressive') == 1
