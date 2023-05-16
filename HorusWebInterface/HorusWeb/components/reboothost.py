import json

from django_unicorn.components import UnicornView
from Main.main import get_PC_by_number
from Main.main import change_boot_order
from Main.main import wake_up_single_host


class ReboothostView(UnicornView):
    pcnumber = int()

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)  # calling super is required
        self.pcnumber = kwargs.get("pcnumber",)
        self.pc = get_PC_by_number(self.pcnumber)

    def reboot(self):
        with open("../../OS.json") as f:
            data = json.loads(f.read().replace('\n', ''))
        systems = []
        for i in data['Operating_Systems']:
            if not i['Systemname'] == self.pc['system']:
                systems += i
        change_boot_order(self.pc['ip'],systems[0]['Systemname'],systems[0]['UserName'],systems[0]['Password'])



    def wakeup(self):
        wake_up_single_host(self.pc['mac'])


