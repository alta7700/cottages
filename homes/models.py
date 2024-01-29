import uuid

from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField


from .validators import validate_16x9_jpeg


def home_cover_path(*_):
    return f'home/covers/{uuid.uuid4()}.jpeg'


class Home(models.Model):
    id = models.AutoField(primary_key=True, editable=False)

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=100, verbose_name='Идентификатор')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    position = models.PositiveIntegerField(null=True, blank=True, verbose_name='Позиция в списке')
    cover = models.ImageField(
        upload_to=home_cover_path, validators=[validate_16x9_jpeg], help_text='Только JPEG 16x9',
        verbose_name='Обложка'
    )
    cost_per_day = models.PositiveIntegerField(verbose_name='Цена за сутки')
    show_on_site = models.BooleanField(default=False, verbose_name='Показывать на сайте')

    short_description = models.TextField(blank=True, default='', verbose_name='Краткое описание')
    long_description = RichTextField(blank=True, default='', verbose_name='Полное описание')

    ya_map = models.TextField(blank=True, default='', verbose_name='Код яндекс карт')
    video = models.TextField(blank=True, default='', verbose_name='Ссылка видео Youtube')

    conv_wifi = models.BooleanField(default=False, verbose_name='Wi-Fi')
    conv_minibar = models.BooleanField(default=False, verbose_name='Минибар')
    conv_parking = models.BooleanField(default=False, verbose_name='Парковка')
    conv_hairdryer = models.BooleanField(default=False, verbose_name='Фен')
    conv_workspace = models.BooleanField(default=False, verbose_name='Рабочая зона')
    conv_safe = models.BooleanField(default=False, verbose_name='Сейф')
    conv_washing_machine = models.BooleanField(default=False, verbose_name='Стиральная машина')
    conv_swimming_pool = models.BooleanField(default=False, verbose_name='Бассейн')

    class Meta:
        db_table = 'homes'
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'
        ordering = ('position', )

    def __str__(self):
        return self.name

    @property
    def conveniences(self):
        return {
            field.name[5:]: field.verbose_name
            for field in self.__class__._meta.local_fields
            if field.name.startswith('conv_') and getattr(self, field.name)
        }

    @property
    def short_description_parts(self):
        return self.short_description.split('\n')


def carousel_image_path(instance: "HomeCarouselImage", *_):
    return f'home/carousel/{instance.id}.jpeg'


class HomeCarouselImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='carousel')
    position = models.PositiveIntegerField(verbose_name='Позиция в карусели')
    name = models.CharField(max_length=30, validators=[MinLengthValidator(1)], blank=False, verbose_name='Название')
    image = models.ImageField(
        upload_to=carousel_image_path, validators=[validate_16x9_jpeg], help_text='Только JPEG 16x9',
        verbose_name='Фото'
    )

    class Meta:
        db_table = 'home_carousel_images'
        verbose_name = 'Дополнительная фотография дома'
        verbose_name_plural = 'Дополнительные фотографии дома (карусель)'
        ordering = ('position',)

    @property
    def url(self) -> str:
        return self.image.url

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height


class Ticket(models.Model):
    class Status(models.IntegerChoices):
        NEW = 1, 'Новая'
        PENDING = 2, 'В обработке'
        CLOSED = 3, 'Закрыта'

    id = models.AutoField(primary_key=True, editable=False)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='tickets', verbose_name='Дом')
    name = models.CharField(max_length=30, default='', blank=True, verbose_name='Имя')
    start_date = models.DateField(verbose_name='Начало брони')
    end_date = models.DateField(verbose_name='Конец брони')
    phone_number = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, verbose_name='Телефон')
    guest_count = models.PositiveSmallIntegerField(verbose_name='Количество гостей')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Отправлено клиентом')
    status = models.PositiveSmallIntegerField(choices=Status, default=Status.NEW, verbose_name='Статус')
    comment = models.TextField(default='', blank=True, verbose_name='Комментарий')

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
