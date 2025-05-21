from external.vbox_server.src.domain.machines.models import VirtualBoxApiResponse, VirtualBoxApiError, FullMachineInfo
from internal.models.machine import Machine, MachineLoadProcessState, MachineLoadSuccessState, MachineLoadErrorState
from internal.models.connection import Connection
from . get_machine_list import GetMachineListController
import collections.abc
import PySide6.QtCore
import requests
import uuid

class DeleteMachineController():
    def exec(self, connection: Connection, machine: Machine) -> collections.abc.Awaitable[None]:
        try:
            machine.machine_state = MachineLoadProcessState()
            response = requests.delete(url = f'http://{connection.connection_destination.host}:{connection.connection_destination.port}/api/v1/machine/{machine.machine_uuid}')
            if response.status_code == 200:
                success_response = VirtualBoxApiResponse[None].model_validate(response.json())
                print(f'[DeleteMachineController][200][{success_response.payload}]')
                GetMachineListController().exec(connection = connection)
            elif response.status_code == 500:
                error_response: VirtualBoxApiError = VirtualBoxApiError.model_validate(response.json())
                print(f'[DeleteMachineController][500][{error_response}]')
                machine.machine_state = MachineLoadErrorState(reason = error_response.error_info.stderr)
        except Exception as error:
            print(f'[DeleteMachineController][error][{error}]')
            machine.machine_state = MachineLoadErrorState(reason = str(error))
