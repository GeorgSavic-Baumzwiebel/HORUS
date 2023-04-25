from django_unicorn.components import UnicornView
from ..tasks import update_status


class UpdatePcsJsonView(UnicornView):

    def update(self):
        print("test123")
        update_status()
