from external.vbox_server.src.domain.machines import FullMachineInfo
from . machine import Machine
import PySide6.QtCore
import pydantic
import typing
import enum
import uuid

class ConnectionDestination(pydantic.BaseModel):
    host: pydantic.constr(min_length = 1)
    port: pydantic.conint(ge = 0, le = 65535)

class ConnectionStateError(pydantic.BaseModel):
    reason: str
class ConnectionStateOnline(pydantic.BaseModel):
    pass
class ConnectionStateOffline(pydantic.BaseModel):
    pass
ConnectionState = ConnectionStateError | ConnectionStateOnline | ConnectionStateOffline | None


class Connection(PySide6.QtCore.QAbstractListModel):
    class ConnectionRoles(enum.IntEnum):
        MACHINE = PySide6.QtCore.Qt.ItemDataRole.UserRole + 1

    connection_state_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal()
    def __init__(self, connection_destination: ConnectionDestination, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(Connection, self).__init__(parent = parent)
        self.__connection_destination: ConnectionDestination = connection_destination
        self.__connection_state: ConnectionState = None
        self.__machines: list[Machine] = []

    @property
    def connection_destination(self) -> ConnectionDestination:
        return self.__connection_destination
    @property
    def is_online(self) -> bool:
        return isinstance(self.connection_state, ConnectionStateOnline)
    @property
    def connection_state(self) -> ConnectionState:
        return self.__connection_state
    @connection_state.setter
    def connection_state(self, new_state: ConnectionState) -> None:
        self.__connection_state = new_state
        self.connection_state_changed.emit()

    def flags(self, index: PySide6.QtCore.QModelIndex) -> int:
        return super(Connection, self).flags(index) | PySide6.QtCore.Qt.ItemFlag.ItemIsEnabled | PySide6.QtCore.Qt.ItemFlag.ItemIsSelectable
    def roleNames(self) -> dict[int, bytes]:
        return { item.value: item.name.lower().encode('utf-8') for item in Connection.ConnectionRoles }
    def rowCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = PySide6.QtCore.QModelIndex()):
        return len(self.__machines)
    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None

        match role:
            case PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self.__machines[index.row()].machine_uuid)
            case Connection.ConnectionRoles.MACHINE:
                return self.__machines[index.row()]
            case _:
                return None

    @property
    def machines(self) -> None:
        return self.__machines
    def update_machine_list(self, machine_uuids: list[uuid.UUID]) -> None:
        new_machines_list: list[Machine] = []
        old_machine_uuids_dict = { machine.machine_uuid: machine for machine in self.__machines }
        for machine_uuid in machine_uuids:
            if machine_uuid in old_machine_uuids_dict: # если машина уже была, можно её оставить
                new_machines_list.append(old_machine_uuids_dict[machine_uuid])
            else: # если машины не было, нужно её добавить
                machine = Machine(machine_uuid = machine_uuid, parent = self)
                machine.machine_state_changed.connect(lambda: self.__on_machine_state_changed(machine = machine))
                new_machines_list.append(machine)

        self.beginResetModel()
        new_machine_uuids_set = set(machine_uuids)
        for machine in self.__machines:
            if machine.machine_uuid not in new_machine_uuids_set:
                machine.deleteLater()
        self.__machines = new_machines_list
        self.endResetModel()
    def find_machine(self, machine_uuid: uuid.UUID) -> Machine | None:
        for machine in self.__machines:
            if machine.machine_uuid == machine_uuid:
                return machine
        else:
            return None
    def __on_machine_state_changed(self, machine: Machine) -> None:
        if (machine_index := self.__machines.index(machine)) != -1:
            self.dataChanged.emit(self.index(machine_index), self.index(machine_index), [])
