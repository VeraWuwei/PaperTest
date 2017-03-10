from django.http import JsonResponse
from threading   import Lock
from django.views.decorators.csrf import csrf_exempt
import json



luns      = []
luns_lock = Lock()

def save_luns_to_file():
    global luns
    with open('./lun.db', 'w') as db_file:
        json.dump(luns, db_file)

def load_luns_from_file():
    global luns
    with open('./lun.db', 'r') as db_file:
        luns = json.load(db_file)

with luns_lock:
    load_luns_from_file()

@csrf_exempt
def custom404(request):
    return JsonResponse({ 'status_code': 404, 'error': 'The resource was not found' })

@csrf_exempt
def custom400(request):
    return JsonResponse({ 'status_code': 400, 'error': 'Bad request' })

@csrf_exempt
def _create_luns(request):
    result   = []
    new_luns = request
    for new_lun in new_luns:
        if not new_lun or not 'name' in new_lun or not 'size' in new_lun or new_lun['size'] <= 0:
            return custom400(request)

    with luns_lock:
        for new_lun in new_luns:
            item = {
                       'id'        : luns[-1]['id'] + 1,
                       'name'      : new_lun['name'],
                       'initiator' : new_lun.get('initiator','default'),
                       'target'    : new_lun.get('target','default'),
                       'size'      : new_lun['size']
                   }

            result.append(item)
            luns.append(item)
            save_luns_to_file()
    return JsonResponse({ "status_code" : 200, "luns" : result }, json_dumps_params={ "indent" : 4 })

@csrf_exempt
def _get_luns(request):
    return JsonResponse({ "status_code" : 200, "luns" : luns }, json_dumps_params={ "indent" : 4 })

@csrf_exempt
def handle_luns(request):
    if request.method == "POST":
        temp=json.load(request)
        if not temp:
            return custom400(request)
        return _create_luns(temp)
    else:
        return _get_luns(request)

@csrf_exempt
def _get_lun(lun):
    return JsonResponse({"status_code" : 200, "lun" : lun}, json_dumps_params={"indent" : 4})

@csrf_exempt
def _get_lun_size(lun):
    return JsonResponse({"status_code" : 200, "lun" : lun["size"]}, json_dumps_params={"indent" : 4})

@csrf_exempt
def _delete_lun(lun):
    luns.remove(lun)
    return JsonResponse({"status_code" : 200}, json_dumps_params={"indent" : 4})
    save_luns_to_file()

@csrf_exempt
def _update_lun(lun, request):
    item=request
    lun['size'] = item['size']
    save_luns_to_file()
    return JsonResponse({"status_code" : 200, "lun" : lun}, json_dumps_params={"indent" : 4})

@csrf_exempt
def handle_lun(request, lun_id):
    with luns_lock:
        # get lun according to lun_id
        lun = filter(lambda x: x['id'] == int(lun_id), luns)
        if len(lun) == 0:
            return custom404(request)
        lun = lun[0]

        if request.method == "PUT":
            temp = json.load(request)
            if not temp:
                return custom400(request)
            return _update_lun(lun, temp)
        elif request.method == "DELETE":
            return _delete_lun(lun)
        else:
            return _get_lun(lun)



@csrf_exempt
def handle_lun_size(request, lun_id):
    with luns_lock:
        # get lun according to lun_id
        lun = filter(lambda x: x['id'] == int(lun_id), luns)
        if len(lun) == 0:
            return custom404(request)
        lun = lun[0]

        if request.method == "PUT":
            temp = json.load(request)
            if not temp:
                return custom400(request)
            return _update_lun(lun, temp)
        else:
            return _get_lun_size(lun)

