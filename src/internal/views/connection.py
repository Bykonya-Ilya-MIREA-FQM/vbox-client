import pydantic
from external.vbox_server.src.domain.machines.models import CreateMachineInfo
from internal.views.utils.current_watching_list_view import CurrentWatchingListView
from internal.views.utils.precise_slider import HorizontalPreciseSlider
from internal.models.connection import Connection
from internal.models.machine import Machine
import internal.models.machine
import PySide6.QtWidgets
import PySide6.QtCore
import uuid

class CreateMachineDialog(PySide6.QtWidgets.QDialog):
    def __init__(self, connection: Connection, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(CreateMachineDialog, self).__init__()
        self.__connection: Connection = connection
        self.__result: CreateMachineInfo | None = None
        
        self.__os_type_edit = PySide6.QtWidgets.QLineEdit(text = 'Linux_64')
        self.__template_edit = PySide6.QtWidgets.QComboBox()
        self.__drive_size_gb_edit = HorizontalPreciseSlider(minimum = 1, maximum = 1_000, tick_size = 10, tick_interval = 100, units = 'gb')
        self.__cpu_count_edit = HorizontalPreciseSlider(minimum = 1, maximum = 8, tick_size = 1, tick_interval = 1, units = 'cpu')
        self.__memory_mb_edit = HorizontalPreciseSlider(minimum = 0, maximum = 4096, tick_size = 128, tick_interval = 128, units = 'mb')
        self.__vram_mb_edit = HorizontalPreciseSlider(minimum = 0, maximum = 256, tick_size = 16, tick_interval = 16, units = 'mb')
        self.__vrde_username = PySide6.QtWidgets.QLineEdit(text = '')
        self.__vrde_password = PySide6.QtWidgets.QLineEdit(text = '')
        self.__reject_button = PySide6.QtWidgets.QPushButton('Cancel')
        self.__accept_button = PySide6.QtWidgets.QPushButton('Ok')

        self.__template_edit.addItem('alpine-virt-3.21.3-x86_64')
        self.__os_type_edit.textChanged.connect(self.__validate_result)
        self.__template_edit.currentIndexChanged.connect(self.__validate_result)
        self.__drive_size_gb_edit.value_changed.connect(self.__validate_result)
        self.__cpu_count_edit.value_changed.connect(self.__validate_result)
        self.__memory_mb_edit.value_changed.connect(self.__validate_result)
        self.__vram_mb_edit.value_changed.connect(self.__validate_result)
        self.__vrde_username.textChanged.connect(self.__validate_result)
        self.__vrde_password.textChanged.connect(self.__validate_result)
        self.__reject_button.clicked.connect(self.reject)
        self.__accept_button.clicked.connect(self.accept)
        
        self.__layout = PySide6.QtWidgets.QGridLayout()
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'OS Type: '), 0, 0, 1, 1)
        self.__layout.addWidget(self.__os_type_edit, 0, 1, 1, 1)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'ISO: '), 1, 0, 1, 1)
        self.__layout.addWidget(self.__template_edit, 1, 1, 1, 1)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'Drive size (GB): '), 2, 0, 1, 1)
        self.__layout.addWidget(self.__drive_size_gb_edit, 2, 1, 1, 1)

        
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'CPU count: '), 3, 0, 1, 1)
        self.__layout.addWidget(self.__cpu_count_edit, 3, 1, 1, 1)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'RAM (mb): '), 4, 0, 1, 1)
        self.__layout.addWidget(self.__memory_mb_edit, 4, 1, 1, 1)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'VRAM (mb): '), 5, 0, 1, 1)
        self.__layout.addWidget(self.__vram_mb_edit, 5, 1, 1, 1)

        
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'VRDE Username'), 6, 0, 1, 1)
        self.__layout.addWidget(self.__vrde_username, 6, 1, 1, 1)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(text = 'VRDE Password'), 7, 0, 1, 1)
        self.__layout.addWidget(self.__vrde_password, 7, 1, 1, 1)

        lifespan_buttons_layout = PySide6.QtWidgets.QHBoxLayout()
        lifespan_buttons_layout.addWidget(self.__reject_button)
        lifespan_buttons_layout.addWidget(self.__accept_button)
        self.__layout.addLayout(lifespan_buttons_layout, 8, 0, 1, 2)
        self.setLayout(self.__layout)
        self.__validate_result()
    
    def create_machine_info(self) -> CreateMachineInfo:
        return self.__result
    
    def __validate_result(self) -> None:
        try:
            self.__result = CreateMachineInfo(
                os_type = self.__os_type_edit.text(),
                template = self.__template_edit.currentText(),
                drive = CreateMachineInfo.DriveInfo(size_gb = self.__drive_size_gb_edit.value()),
                hardware = CreateMachineInfo.HardwareInfo(
                    cpu_count = self.__cpu_count_edit.value(), 
                    memory_mb = self.__memory_mb_edit.value(), 
                    vram_mb = self.__vram_mb_edit.value()
                ),
                vrde_credentials = CreateMachineInfo.VrdeCredentialsInfo(
                    username = self.__vrde_username.text(), 
                    password = self.__vrde_password.text()
                )
            )
            self.__accept_button.setEnabled(True)
        except pydantic.ValidationError as error:
            self.__result = None
            self.__accept_button.setEnabled(False)
    
    @classmethod
    def __round_to_nearest(number, multiple):
        return multiple * round(number / multiple)



class ConnectionView(PySide6.QtWidgets.QWidget):
    current_machine_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Machine)
    create_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, CreateMachineInfo)
    update_all_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection)
    update_one_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    delete_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    start_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    stop_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(ConnectionView, self).__init__(parent = parent)
        self.__list_view = CurrentWatchingListView()
        self.__list_view.setSelectionBehavior(PySide6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.__list_view.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.__list_view.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__list_view.setEditTriggers(PySide6.QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.__list_view.setContextMenuPolicy(PySide6.QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.__list_view.customContextMenuRequested.connect(self.__show_list_item_menu)
        self.__list_view.current_item_changed.connect(lambda index: self.current_machine_changed.emit(index.data(role = Connection.ConnectionRoles.MACHINE)))

        self.__create_machine_button = PySide6.QtWidgets.QPushButton('➕')
        self.__create_machine_button.clicked.connect(self.__create_machine)
        self.__update_all_machine_button = PySide6.QtWidgets.QPushButton('🔄')
        self.__update_all_machine_button.clicked.connect(self.__update_all_machine)

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__button_layout = PySide6.QtWidgets.QHBoxLayout()
        self.__button_layout.addWidget(self.__create_machine_button)
        self.__button_layout.addWidget(self.__update_all_machine_button)
        self.__layout.addLayout(self.__button_layout)
        self.__layout.addWidget(self.__list_view)
        self.setLayout(self.__layout)
        
        self.resetConnection()

    def resetConnection(self, connection: Connection | None = None) -> None:
        self.__list_view.setModel(connection)

    def __create_machine(self):
        if self.__list_view.model() is None:
            return
        if (create_machine_dialog := CreateMachineDialog(connection = self.__list_view.model(), parent = self)).exec() == PySide6.QtWidgets.QDialog.DialogCode.Accepted:
            self.create_machine_request.emit(self.__list_view.model(), create_machine_dialog.create_machine_info())
    def __update_one_machine(self, machine: Machine):
        if self.__list_view.model() is None:
            return
        self.update_one_machine_request.emit(self.__list_view.model(), machine)
    def __update_all_machine(self):
        if self.__list_view.model() is None:
            return
        self.update_all_machine_request.emit(self.__list_view.model())
    def __delete_machine(self, machine: Machine):
        if self.__list_view.model() is None:
            return
        if PySide6.QtWidgets.QMessageBox.question(self, 'Delete machine', 'Are you sure?') == PySide6.QtWidgets.QMessageBox.StandardButton.Yes:
            self.delete_machine_request.emit(self.__list_view.model(), machine)
    
    def __show_list_item_menu(self, position: PySide6.QtCore.QPoint) -> None:
        item_index = self.__list_view.indexAt(position)
        if not item_index.isValid():
            return

        machine: Machine = item_index.data(role = Connection.ConnectionRoles.MACHINE)
        if machine is None:
            return

        list_item_menu = PySide6.QtWidgets.QMenu(parent = self)
        start_machine_action = list_item_menu.addAction('▶️ Start')
        stop_machine_action = list_item_menu.addAction('⏸️ Stop')
        match type(machine.machine_state):
            case internal.models.machine.MachineLoadSuccessState:
                start_machine_action.triggered.connect(lambda: self.start_machine_request.emit(self.__list_view.model(), machine))
                stop_machine_action.triggered.connect(lambda: self.stop_machine_request.emit(self.__list_view.model(), machine))
                start_machine_action.setEnabled(not machine.machine_state.info.is_online)
                stop_machine_action.setEnabled(machine.machine_state.info.is_online)
            case internal.models.machine.MachineLoadProcessState | internal.models.machine.MachineLoadErrorState | _:
                start_machine_action.setEnabled(False)
                stop_machine_action.setEnabled(False)
        list_item_menu.addAction('🔄 Update').triggered.connect(lambda: self.__update_one_machine(machine = machine))
        list_item_menu.addAction('🗑️ Delete').triggered.connect(lambda: self.__delete_machine(machine = machine))
        list_item_menu.exec(self.__list_view.mapToGlobal(position))
