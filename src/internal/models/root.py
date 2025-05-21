from . connection import Connection, ConnectionDestination
import PySide6.QtCore
import pydantic
import typing
import enum




class Root(PySide6.QtCore.QAbstractListModel):
    class RootRoles(enum.IntEnum):
        CONNECTION = PySide6.QtCore.Qt.ItemDataRole.UserRole + 1
        # CONNECTION_STATUS = enum.auto()
        # CONNECTION_INFO = enum.auto()
        # MACHINE_MODEL = enum.auto()
        # IS_ONLINE = enum.auto()
        # HOST = enum.auto()
        # PORT = enum.auto()

    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(Root, self).__init__(parent = parent)
        self.__connections: list[Connection] = []

    def flags(self, index: PySide6.QtCore.QModelIndex) -> int:
        return super(Root, self).flags(index) | PySide6.QtCore.Qt.ItemFlag.ItemIsEnabled | PySide6.QtCore.Qt.ItemFlag.ItemIsSelectable
    def roleNames(self) -> dict[int, bytes]:
        return { item.value: item.name.lower().encode('utf-8') for item in Root.RootRoles }
    def rowCount(self, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = PySide6.QtCore.QModelIndex()):
        return len(self.__connections)
    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None
        match role:
            case PySide6.QtCore.Qt.ItemDataRole.DisplayRole:
                return f'{"🟩" if self.__connections[index.row()].is_online else "🟥"} {self.__connections[index.row()].connection_destination.host}:{self.__connections[index.row()].connection_destination.port}'
            case Root.RootRoles.CONNECTION:
                return self.__connections[index.row()]
            case _:
                return None

    def create_connection(self, connection_destination: ConnectionDestination) -> Connection:
        if (connection_index := self.__index_at_connection_destination(connection_destination = connection_destination)) != -1:
            return self.__connections[connection_index]

        self.beginInsertRows(PySide6.QtCore.QModelIndex(), len(self.__connections), len(self.__connections))
        connection = Connection(connection_destination = connection_destination, parent = self)
        connection.connection_state_changed.connect(lambda: self.__on_connection_info_changed(connection = connection))
        self.__connections.append(connection)
        self.endInsertRows()
        return connection
    def delete_connection(self, connection_destination: ConnectionDestination) -> None:
        if (connection_index := self.__index_at_connection_destination(connection_destination = connection_destination)) != -1:
            self.beginRemoveRows(PySide6.QtCore.QModelIndex(), connection_index, connection_index)
            self.__connections[connection_index].deleteLater()
            del self.__connections[connection_index]
            self.endRemoveRows()
    def find_connection(self, connection_destination: ConnectionDestination) -> Connection | None:
        if (connection_index := self.__index_at_connection_destination(connection_destination = connection_destination)) != -1:
            return self.__connections[connection_index]
        else:
            return None
    def __on_connection_info_changed(self, connection: Connection) -> None:
        if (connection_index := self.__connections.index(connection)) != -1:
            self.dataChanged.emit(self.index(connection_index), self.index(connection_index), [])
    def __index_at_connection_destination(self, connection_destination: ConnectionDestination) -> int:
        for index, connection in enumerate(self.__connections):
            if connection_destination == connection.connection_destination:
                return index
        return -1
