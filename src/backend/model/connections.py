from more_itertools import first, last
from . machines import MachinesModel
import PySide6.QtCore
import pydantic
import typing
import enum

class ConnectionInfo(pydantic.BaseModel):
    host: pydantic.constr(min_length = 1)
    port: pydantic.conint(ge = 0, le = 655535)

class ConnectionsModel(PySide6.QtCore.QAbstractListModel):
    class ConnectionsModelRoles(enum.IntEnum):
        MACHINE_MODEL = PySide6.QtCore.Qt.ItemDataRole.UserRole + 1
        IS_ONLINE = enum.auto()
        HOST = enum.auto()
        PORT = enum.auto()

    def __init__(self, connections: list[tuple[ConnectionInfo, MachinesModel]], parent: PySide6.QtCore.QObject | None = None) -> None:
        super(ConnectionsModel, self).__init__(parent = parent)
        self.__connections: list[tuple[ConnectionInfo, MachinesModel]] = connections

    def flags(self, index: PySide6.QtCore.QModelIndex) -> int:
        return super().flags(index) | PySide6.QtCore.Qt.ItemFlag.ItemIsEnabled | PySide6.QtCore.Qt.ItemFlag.ItemIsSelectable
    def roleNames(self) -> dict[int, bytes]:
        return { item.value: item.name.lower().encode('utf-8') for item in ConnectionsModel.ConnectionsModelRoles }
    def rowCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = PySide6.QtCore.QModelIndex()):
        return len(self.__connections)
    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None
        match role:
            case PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
                return f'{self.__connections[index.row()][0].host}:{self.__connections[index.row()][0].port}'
            case PySide6.QtCore.Qt.ItemDataRole.CheckStateRole:
                match index.row() % 3:
                    case 0:
                        return PySide6.QtCore.Qt.CheckState.Checked
                    case 1:
                        return PySide6.QtCore.Qt.CheckState.Unchecked
                    case 2:
                        return PySide6.QtCore.Qt.CheckState.PartiallyChecked
                # return PySide6.QtCore.Qt.CheckState.Checked if self.__connections[index.row()][1].is_online else PySide6.QtCore.Qt.CheckState.Unchecked
            case ConnectionsModel.ConnectionsModelRoles.MACHINE_MODEL:
                return self.__connections[index.row()][1]
            case ConnectionsModel.ConnectionsModelRoles.IS_ONLINE:
                return 
            case ConnectionsModel.ConnectionsModelRoles.HOST:
                return self.__connections[index.row()][0].host
            case ConnectionsModel.ConnectionsModelRoles.PORT:
                return self.__connections[index.row()][0].port
            case _:
                return None
    
    def add_new_connection(self, connection: ConnectionInfo) -> None:
        for exists_connection_info, exists_connection_model in self.__connections:
            if connection == exists_connection_info:
                return

        self.beginInsertRows(PySide6.QtCore.QModelIndex(), len(self.__connections), len(self.__connections))
        self.__connections.append((connection, MachinesModel(machines = [])))
        self.endInsertRows()
    def delete_connection(self, index: int) -> None:
        if index >= 0 and index < len(self.__connections):
            self.beginRemoveRows(PySide6.QtCore.QModelIndex(), index, index)
            del self.__connections[index]
            self.endRemoveRows()