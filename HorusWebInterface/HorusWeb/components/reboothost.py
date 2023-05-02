from django_unicorn.components import UnicornView


class ReboothostView(UnicornView):
    pcnumber = "World"

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.pcnumber = kwargs.get("pcnumber",)

    def reboot(self):
        print(self.pcnumber)

    def wakeup(self):
        print("test123")
