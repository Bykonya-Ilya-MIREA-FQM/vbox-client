from internal.models.connection import Connection, ConnectionStateOnline, ConnectionStateOffline, ConnectionStateError
from . get_machine_list import GetMachineListController
from internal.models.root import Root
import collections.abc
import requests

class GetConnectionStatusController:
    def exec(self, connection: Connection) -> collections.abc.Awaitable[None]:
        try:   
            response = requests.get(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/ping')
            print(f'[GetConnectionStatusController][Result][{response.status_code}]')
            if response.status_code == 200:
                connection.connection_state = ConnectionStateOnline()
                GetMachineListController().exec(connection = connection)
            else:
                connection.connection_state = ConnectionStateOffline()
        except Exception as error:
            print(f'[GetConnectionStatusController][Error][{error}]')
            connection.connection_state = ConnectionStateError(reason = str(error))
