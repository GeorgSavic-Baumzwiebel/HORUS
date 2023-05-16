import json


# from celery import shared_task

from Main.main import check_status
from Main.main import check_OperatingSystem
from multiprocessing import Pool, freeze_support

def update_status():
    with open('PCs.json', 'r') as f:
        data = json.loads(f.read().replace('\n', ''))
    pool = Pool()
    ips = [x['ip'] for x in data['pcs']]
    pool.map(check_status, ips)
    pool.map(check_OperatingSystem, ips)
    # for pc in data['pcs']:
        # pc['status'] = check_status(pc['ip'])
        # pc['system'] = check_OperatingSystem(pc['ip'])
    with open('PCs.json', 'w') as f:
        json.dump(data, f,indent=4)