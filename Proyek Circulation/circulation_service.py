import json
from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler
from nameko.web.handlers import http

import dependenciesCirculation

class CirculationService:
    name="circulation_service"

    database = dependenciesCirculation.Database()

    

    #Publish Subscribe
    dispatch = EventDispatcher()

    #Handle Event  (Orchestration)
    @event_handler("orchestration_service", "circulation_event")
    def handle_event_method(self, payload):
        print(payload)


    @http('GET','/room_item_by_id/<int:id_room>/<int:id_item>')
    def get_room_item_by_id(self, request, id_room, id_item):
        room_item = self.get_room_item_by_id(id_room, id_item)
        return json.dumps({'result': room_item})

    @http('POST', '/room_item')
    def add_room_item(self, request):
        data = json.loads(request.get_data(as_text=True))
        new_room_item = self.add_room_item(data['id_room'], data['id_item'])
        return new_room_item

    @http('POST', '/circulation')
    def add_circulation(self, request):
        data = json.loads(request.get_data(as_text=True))
        new_circulaton = self.add_circulation(data['id_room'], data['id_item'],  data['id_employee'], data['id_purchase'], data['qty'], data['date'], data['status'])
        return new_circulaton

    @rpc
    def get_room_item_by_id(self, id_room, id_item):
        room_item = self.database.get_room_item_by_id(id_room, id_item)
        return room_item

    @rpc
    def add_room_item(self, id_room, id_item, qty):
        new_room_item = self.database.add_room_item(id_room, id_item, qty)
        return new_room_item

    @rpc
    def add_circulation(self, id_room, id_item, id_employee, id_purchase, qty, status):
        new_circulation = self.database.add_circulation(id_room, id_item, id_employee, id_purchase, qty, status)
        return new_circulation

    