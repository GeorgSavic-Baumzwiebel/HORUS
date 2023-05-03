from django.http import HttpResponse
from django.template import loader
import json


from Main.main import check_status
from .tasks import update_status


def index(request):
    if request.path == "/":
        # update_status()
        with open('PCs.json', 'r') as f:
            data = json.loads(f.read().replace('\n', ''))
        table = list()
        for counter, pc in enumerate(data["pcs"]):
            ip = pc['ip']
            mac = pc['mac']
            number = pc['number']
            status = pc['status']
            system = pc['system']
            table.append(number)
            table.append(mac)
            table.append(ip)
            if status:
                table.append("up")
            else:
                table.append("down")
            table.append(system)
            table.append(counter + 1)
        context = {
            'results': table,
        }
        print(context)
        for r in context.get('results'):
            print(r)
        template = loader.get_template("site/index.html")
        return HttpResponse(template.render(context, request))
