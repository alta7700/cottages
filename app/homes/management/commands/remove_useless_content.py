import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from homes.models import Home, HomeCarouselImage


class Command(BaseCommand):
    help = 'remove useless photo. For use in cron.'

    def handle(self, *args, **options):
        remove_useless(
            settings.MEDIA_ROOT / settings.HOME_COVERS_FOLDER,
            set(settings.MEDIA_ROOT / cover for cover in Home.objects.all().values_list('cover', flat=True)),
        )
        remove_useless(
            settings.MEDIA_ROOT / settings.HOME_CAROUSEL_IMAGES_FOLDER,
            set(settings.MEDIA_ROOT / img for img in HomeCarouselImage.objects.all().values_list('image', flat=True)),
        )


def remove_useless(folder: Path, in_use: set[str]):
    if not (folder.exists() and folder.is_dir()):
        return
    for file in os.listdir(folder):
        file_path = folder / file
        if not os.path.isfile(file_path):
            continue
        if file_path not in in_use:
            os.remove(file_path)
