from nameko.rpc import rpc, RpcProxy
from nameko.events import EventDispatcher, event_handler 

class OrchestrationService:
    name = "orchestration_service"

    circulation_service = RpcProxy('circulation_service')

    #Publish Subscribe
    dispatch = EventDispatcher()

    result1 = {
        'add_circulation_result': None
    }
    result2 = {
        'add_room_item_result': None
    }
    result3 = {
        'room_item_by_id': None
    }

    #Cth Pub Subs
    @rpc 
    def dispatch_method(self, payload):
        self.dispatch("circulation_event", payload)

    # Orchestration
    @rpc
    def add_circulation_method(self, id_room, id_item, id_employee, id_purchase, qty, status):
        result1 = {
            'add_circulation_result' : self.circulation_service.add_circulation(id_room, id_item, id_employee, id_purchase, qty, status),
        }

        return result1

    # Orchestration
    @rpc
    def add_room_item_method(self, id_room, id_item, qty):
        result2 = {
            'add_room_item_result' : self.circulation_service.add_room_item(id_room, id_item, qty)
        }

        return result2

    # Orchestration
    @rpc
    def get_room_item_method(self, id_room, id_item):
        result3 = {
            'room_item_by_id' : self.circulation_service.get_room_item_by_id(id_room, id_item)
        }

        return result3