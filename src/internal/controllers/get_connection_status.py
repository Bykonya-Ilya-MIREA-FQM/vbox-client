import pydantic
from external.vbox_server.src.domain.machines.models import VirtualBoxApiResponse
from internal.models.connection import Connection, ConnectionStateOnline, ConnectionStateOffline, ConnectionStateError
from . get_machine_list import GetMachineListController
from internal.models.root import Root
import collections.abc
import requests
import uuid

class GetConnectionStatusController:
    def exec(self, connection: Connection) -> collections.abc.Awaitable[None]:
        try:   
            response = requests.get(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/ping')
            print(f'[GetConnectionStatusController][Result][{response.status_code}]')
            if response.status_code != 200:
                connection.connection_state = ConnectionStateOffline()
                return

            response = requests.get(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/api/v1/image')
            response.raise_for_status()
            
            success_response = pydantic.TypeAdapter(list[str]).validate_json(response.text)
            connection.connection_state = ConnectionStateOnline(templates = success_response)
            GetMachineListController().exec(connection = connection)            
        except Exception as error:
            print(f'[GetConnectionStatusController][Error][{error}]')
            connection.connection_state = ConnectionStateError(reason = str(error))
