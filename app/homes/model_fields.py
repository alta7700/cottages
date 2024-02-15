from django.db import models

from . import utils


class ProgressiveJpegField(models.ImageField):
    def pre_save(self, model_instance, add):
        file = super(models.FileField, self).pre_save(model_instance, add)
        if not utils.is_progressive_jpeg(file.file):
            file.file = utils.make_progressive_jpeg(file.file)
        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save(file.name, file.file, save=False)
        return file
