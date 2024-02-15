import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from homes import utils


class Command(BaseCommand):
    help = 'Convert all old non-progressive jpeg to progressive'

    def handle(self, *args, **options):
        convert_to_progressive(settings.MEDIA_ROOT / settings.HOME_COVERS_FOLDER)
        convert_to_progressive(settings.MEDIA_ROOT / settings.HOME_CAROUSEL_IMAGES_FOLDER)


def convert_to_progressive(folder: Path):
    if not (folder.exists() and folder.is_dir()):
        return
    for file in os.listdir(folder):
        file_path = folder / file
        if not os.path.isfile(file_path):
            continue
        if not utils.is_progressive_jpeg(file_path):
            file = utils.make_progressive_jpeg(file_path)
            with open(file_path, 'wb') as f:
                f.write(file.getbuffer())
            print(file_path)
