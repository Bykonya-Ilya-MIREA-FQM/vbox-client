# from external.vbox_server.src.domain.machines.models import FullMachineInfo, VrdeConnectionInfo, VBoxManageCallResult
# import PySide6.QtCore
# import aiohttp
# import asyncio
# import json
# import uuid

# class BaseFetchVmInfoTask(PySide6.QtCore.QThread):
#     def __init__(self, host: str, parent: PySide6.QtCore.QObject | None = None) -> None:
#         super().__init__(parent = parent)
#         self.__host: str = host
#     async def fetch_one_vm(self, session: aiohttp.ClientSession, machine_uuid: uuid.UUID) -> FullMachineInfo | tuple[str, VBoxManageCallResult] | str:
#         async with session.get(f'{self.__host}/api/v1/machine/{machine_uuid}') as response:
#             match response.status:
#                 case 200:
#                     return FullMachineInfo.model_validate(json.loads(response.content)['payload'])
#                 case 500:
#                     response_json = json.loads(response.content)
#                     if 'stage' in response_json and 'call' in response_json:
#                         return response_json['stage'], VBoxManageCallResult.model_validate(response_json['call'])
#             return response.content.decode('utf-8')
        
# class FetchOneVmInfoTask(BaseFetchVmInfoTask):
#     def __init__(self, machine_uuid: uuid.UUID, host: str, parent: PySide6.QtCore.QObject | None = None) -> None:
#         super().__init__(host = host, parent = parent)
#         self.__machine_uuid:  uuid.UUID = machine_uuid
#     def run(self) -> None:
#         asyncio.run(self.fetch_one_vm())

# class FerchOneVmInfoTask(PySide6.QtCore.QThread):
#     def run(self) -> None:
#         asyncio.run(self.__fetch_info())
#     async def __fetch_info(self, host: str, machine_id: uuid.UUID): 
#         async with aiohttp.ClientSession() as session:
#             async with session.get('http://httpbin.org/get') as resp:
#                 print(resp.status)
#                 print(await resp.text())

# class FerchAllVmInfoTask(PySide6.QtCore.QThread):
#     def run(self) -> None:
#         asyncio.run(self.__fetch_info())
#     def __fetch_info(self, host: str):
#         async with aiohttp.ClientSession() as session:
#             async with session.get('http://httpbin.org/get') as resp:
#                 print(resp.status)
#                 print(await resp.text())

# class VmServerApi(PySide6.QtCore.QObject):
#     def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
#         super().__init__(parent = parent)

#     def update_one_vm_info(self, machine_id: uuid.UUID) -> None:
#         pass
#     def update_all_vm_info(self) -> None:
#         pass
