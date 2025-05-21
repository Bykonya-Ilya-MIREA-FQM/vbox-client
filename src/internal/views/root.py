from internal.views.utils.current_watching_list_view import CurrentWatchingListView
from internal.models.connection import Connection, ConnectionDestination
from internal.models.root import Root
import PySide6.QtWidgets
import PySide6.QtCore
import PySide6.QtGui


class CreateConnectionDialog(PySide6.QtWidgets.QDialog):
    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(CreateConnectionDialog, self).__init__()
        
        self.__host_edit = PySide6.QtWidgets.QLineEdit(text = '127.0.0.1')
        self.__port_edit = PySide6.QtWidgets.QSpinBox(minimum = 0, maximum = 65536)
        self.__reject_button = PySide6.QtWidgets.QPushButton('Cancel')
        self.__accept_button = PySide6.QtWidgets.QPushButton('Ok')

        self.__reject_button.clicked.connect(self.reject)
        self.__accept_button.clicked.connect(self.accept)
        
        self.__layout = PySide6.QtWidgets.QGridLayout()
        self.__layout.addWidget(self.__host_edit, 0, 0, 1, 2)
        self.__layout.addWidget(self.__port_edit, 1, 0, 1, 2)
        self.__layout.addWidget(self.__reject_button, 2, 0, 1, 1)
        self.__layout.addWidget(self.__accept_button, 2, 1, 1, 1)
        self.setLayout(self.__layout)
    
    def connection_info(self) -> ConnectionDestination:
        return ConnectionDestination(
            port = self.__port_edit.value(),
            host = self.__host_edit.text()
        )


class RootView(PySide6.QtWidgets.QWidget):
    current_connection_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection)
    create_connection_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(ConnectionDestination)
    update_connection_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection)
    delete_connection_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection)
    def __init__(self, model: Root, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(RootView, self).__init__(parent = parent)
        self.__list_view = CurrentWatchingListView()
        self.__list_view.setSelectionBehavior(PySide6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.__list_view.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.__list_view.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__list_view.setContextMenuPolicy(PySide6.QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.__list_view.customContextMenuRequested.connect(self.__show_list_item_menu)
        self.__list_view.current_item_changed.connect(lambda index: self.current_connection_changed.emit(index.data(role = Root.RootRoles.CONNECTION)))

        self.__create_connection_button = PySide6.QtWidgets.QPushButton('➕')
        self.__create_connection_button.clicked.connect(self.__create_connection)
        self.__update_current_connection_button = PySide6.QtWidgets.QPushButton('🔄')
        self.__update_current_connection_button.clicked.connect(self.__update_current_connection)
        self.__delete_current_connection_button = PySide6.QtWidgets.QPushButton('🗑️')
        self.__delete_current_connection_button.clicked.connect(self.__delete_current_connection)

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__button_layout = PySide6.QtWidgets.QHBoxLayout()
        self.__button_layout.addWidget(self.__create_connection_button)
        self.__button_layout.addWidget(self.__update_current_connection_button)
        self.__button_layout.addWidget(self.__delete_current_connection_button)
        self.__layout.addLayout(self.__button_layout)
        self.__layout.addWidget(self.__list_view)
        self.setLayout(self.__layout)
        
        self.resetMachineModel(model = model)

    def resetMachineModel(self, model: Root | None = None) -> None:
        self.__list_view.setModel(model)


    def __create_connection(self):
        if (create_connection_dialog := CreateConnectionDialog(parent = self)).exec() == PySide6.QtWidgets.QDialog.DialogCode.Accepted:
            self.create_connection_request.emit(create_connection_dialog.connection_info())
    def __update_current_connection(self):
        if self.__list_view.currentIndex().isValid():
            self.update_connection_request.emit(self.__list_view.currentIndex().data(role = Root.RootRoles.CONNECTION))
    def __delete_current_connection(self):
        if PySide6.QtWidgets.QMessageBox.question(self, 'Remove connection', 'Are you sure?') == PySide6.QtWidgets.QMessageBox.StandardButton.Yes:
            if self.__list_view.currentIndex().isValid():
                self.delete_connection_request.emit(self.__list_view.currentIndex().data(role = Root.RootRoles.CONNECTION))
    def __show_list_item_menu(self, position: PySide6.QtCore.QPoint) -> None:
        item_index = self.__list_view.indexAt(position)
        if not item_index.isValid():
            return

        list_item_menu = PySide6.QtWidgets.QMenu(parent = self)
        list_item_menu.addAction('🔄 Update').triggered.connect(lambda: self.update_connection_request.emit(item_index.data(role = Root.RootRoles.CONNECTION)))
        list_item_menu.addAction('🗑️ Delete').triggered.connect(lambda: self.delete_connection_request.emit(item_index.data(role = Root.RootRoles.CONNECTION)))
        list_item_menu.exec(self.__list_view.mapToGlobal(position))
