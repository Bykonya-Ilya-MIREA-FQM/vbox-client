from external.vbox_server.src.domain.machines.models import VirtualBoxApiResponse, VirtualBoxApiError
from . get_machine_info import GetMachineInfoController
from internal.models.connection import Connection
import collections.abc
import PySide6.QtCore
import requests
import uuid

class GetMachineListController:
    def exec(self, connection: Connection) -> collections.abc.Awaitable[None]:
        try:
            response = requests.get(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/api/v1/machine')
            if response.status_code == 200:
                success_response = VirtualBoxApiResponse[list[uuid.UUID]].model_validate(response.json())
                print(f'[GetMachineListController][200][{success_response.payload}]')
                connection.update_machine_list(machine_uuids = success_response.payload)
                for machine in connection.machines:
                    GetMachineInfoController().exec(connection = connection, machine = machine)
            elif response.status_code == 500:
                error_response = VirtualBoxApiError.model_validate(response.json())
                print(f'[GetMachineListController][500][{error_response}]')
                connection.update_machine_list(machine_uuids = [])
        except Exception as error:
            print(f'[GetMachineListController][error][{error}]')
            connection.update_machine_list(machine_uuids = [])
