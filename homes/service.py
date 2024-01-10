from homes.models import Home


__all__ = ["HomeService"]


class HomeService:
    def __init__(self, instance: Home):
        self.instance = instance

    @classmethod
    def get_available_homes(cls):
        return Home.objects.filter(show_on_site=True).order_by('position')

    @classmethod
    def get_available_homes_details(cls):
        return cls.get_available_homes().prefetch_related('carousel')
