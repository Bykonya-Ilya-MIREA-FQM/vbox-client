from frontend.utils.current_watching_list_view import CurrentWatchingListView
import backend.model.connections
import PySide6.QtWidgets
import PySide6.QtCore

class AddConnectionDialog(PySide6.QtWidgets.QDialog):
    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(AddConnectionDialog, self).__init__()
        
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
    
    def connection_info(self) -> backend.model.connections.ConnectionInfo:
        return backend.model.connections.ConnectionInfo(
            port = self.__port_edit.value(),
            host = self.__host_edit.text()
        )

class ConnectionsView(PySide6.QtWidgets.QWidget):
    current_connection_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(PySide6.QtCore.QModelIndex)
    def __init__(self, model: backend.model.connections.ConnectionsModel, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(ConnectionsView, self).__init__(parent = parent)
        self.__list_view = CurrentWatchingListView()
        self.__list_view.setSelectionBehavior(PySide6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.__list_view.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.__list_view.current_item_changed.connect(self.current_connection_changed.emit)

        self.__add_new_connection_button = PySide6.QtWidgets.QPushButton('+')
        self.__delete_connection_button = PySide6.QtWidgets.QPushButton('-')
        self.__add_new_connection_button.clicked.connect(self.add_new_connection)
        self.__delete_connection_button.clicked.connect(self.delete_connection)

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__button_layout = PySide6.QtWidgets.QHBoxLayout()
        self.__button_layout.addWidget(self.__add_new_connection_button)
        self.__button_layout.addWidget(self.__delete_connection_button)
        self.__layout.addLayout(self.__button_layout)
        self.__layout.addWidget(self.__list_view)
        self.setLayout(self.__layout)
        
        self.resetMachineModel(model = model)

    def resetMachineModel(self, model: backend.model.connections.ConnectionsModel | None = None) -> None:
        self.__list_view.setModel(model)
    def add_new_connection(self):
        if (add_connection_dialog := AddConnectionDialog(parent = self)).exec() == PySide6.QtWidgets.QDialog.DialogCode.Accepted:
            self.__list_view.model().add_new_connection(add_connection_dialog.connection_info())
    def delete_connection(self):
        if PySide6.QtWidgets.QMessageBox.question(self, 'Remove connection', 'Are you sure?') == PySide6.QtWidgets.QMessageBox.StandardButton.Yes:
            self.__list_view.model().delete_connection(index = self.__list_view.currentIndex().row())
