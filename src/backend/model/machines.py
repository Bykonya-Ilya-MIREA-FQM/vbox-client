from external.vbox_server.src.domain.machines import FullMachineInfo
import PySide6.QtCore
import pydantic
import typing
import enum
import uuid

class MachineLoadProcessState(pydantic.BaseModel):
    pass
class MachineLoadSuccessState(pydantic.BaseModel):
    info: FullMachineInfo
class MachineLoadErrorState(pydantic.BaseModel):
    reason: str

class MachinesModel(PySide6.QtCore.QAbstractListModel):
    class MachinesModelRoles(enum.IntEnum):
        UUID = PySide6.QtCore.Qt.ItemDataRole.UserRole + 1
        STATE = enum.auto()

    def __init__(self, is_online: bool, machines: list[tuple[uuid.UUID, MachineLoadProcessState | MachineLoadSuccessState | MachineLoadErrorState]], parent: PySide6.QtCore.QObject | None = None) -> None:
        super(MachinesModel, self).__init__(parent = parent)
        self.__machines: list[tuple[uuid.UUID, MachineLoadProcessState | MachineLoadSuccessState | MachineLoadErrorState]] = machines
        self.__is_online: bool = is_online

    @property
    def is_online(self) -> bool:
        return self.__is_online

    def roleNames(self) -> dict[int, bytes]:
        return { item.value: item.name.lower().encode('utf-8') for item in MachinesModel.MachinesModelRoles }
    def rowCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = PySide6.QtCore.QModelIndex()):
        return len(self.__machines)
    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None

        match role:
            case PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self.__machines[index.row()][0])
            case MachinesModel.MachinesModelRoles.UUID:
                return self.__machines[index.row()][0]
            case MachinesModel.MachinesModelRoles.STATE:
                return self.__machines[index.row()][1]
        return None
