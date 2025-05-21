from external.vbox_server.src.domain.machines.models import VirtualBoxApiResponse, VBoxManageCallResult, CreateMachineInfo
from internal.models.machine import Machine, MachineLoadProcessState, MachineLoadSuccessState, MachineLoadErrorState
from internal.models.connection import Connection
from . get_machine_list import GetMachineListController
import collections.abc
import PySide6.QtCore
import requests
import uuid

class CreateMachineController():
    def exec(self, connection: Connection, machine_info: CreateMachineInfo) -> collections.abc.Awaitable[None]:
        try:
            response = requests.post(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/api/v1/machine', data = machine_info.model_dump_json())
            if response.status_code == 200:
                success_response = VirtualBoxApiResponse[uuid.UUID].model_validate(response.json())
                print(f'[CreateMachineController][200][{success_response.payload}]')
                GetMachineListController().exec(connection = connection)
            elif response.status_code == 500:
                error_response: VBoxManageCallResult = VBoxManageCallResult.model_validate(response.json()['call'])
                print(f'[CreateMachineController][500][{error_response}]')
        except Exception as error:
            print(f'[CreateMachineController][error][{error}]')
