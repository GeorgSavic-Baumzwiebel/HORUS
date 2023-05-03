from django_unicorn.components import UnicornView
from Main.main import get_PC_by_number
from Main.main import check_OperatingSystem
from Main.main import change_boot_order


class ReboothostView(UnicornView):
    pcnumber = int()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.pcnumber = kwargs.get("pcnumber",)

    def reboot(self):
        pc = get_PC_by_number(self.pcnumber)


    def wakeup(self):
        print("test123")
