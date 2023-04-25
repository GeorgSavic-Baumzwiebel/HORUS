import json

from background_task import background
# from celery import shared_task

from Main.main import check_status

def update_status():
    with open('PCs.json', 'r') as f:
        data = json.loads(f.read().replace('\n', ''))
    for pc in data['pcs']:
        pc['status'] = check_status(pc['ip'])
    print(data)
    with open('PCs.json', 'w') as f:
        json.dump(data, f)