from external.vbox_server.src.domain.machines import FullMachineInfo
import PySide6.QtCore
import pydantic
import typing
import uuid

class MachineLoadProcessState(pydantic.BaseModel):
    pass
class MachineLoadSuccessState(pydantic.BaseModel):
    info: FullMachineInfo
class MachineLoadErrorState(pydantic.BaseModel):
    reason: str
MachineState = MachineLoadProcessState | MachineLoadSuccessState | MachineLoadErrorState | None

class Machine(PySide6.QtCore.QObject):
    machine_state_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal()
    def __init__(self, machine_uuid: uuid.UUID, parent: PySide6.QtCore.QObject | None = None) -> None:
        super().__init__(parent = parent)
        self.__machine_uuid: uuid.UUID = machine_uuid
        self.__machine_state: MachineState = None

    @property
    def machine_state(self) -> MachineState:
        return self.__machine_state
    @machine_state.setter
    def machine_state(self, new_state: MachineState) -> None:
        self.__machine_state = new_state
        self.machine_state_changed.emit()
    @property
    def machine_uuid(self) -> uuid.UUID:
        return self.__machine_uuid
