__author__ = 'Marek Mackiewicz'

from django.http import HttpResponse
import json

class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = json.dumps(data)
        super(JsonResponse, self).__init__(content=content, mimetype='application/json')
