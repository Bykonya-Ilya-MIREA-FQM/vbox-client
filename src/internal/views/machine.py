from csv import Error
from internal.models.connection import Connection
from internal.models.machine import Machine, MachineLoadProcessState, MachineLoadSuccessState, MachineLoadErrorState
import internal.models.machine
import PySide6.QtWidgets
import PySide6.QtCore
import uuid


class MachineLoadSuccessStateView(PySide6.QtWidgets.QWidget):
    start_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal()
    stop_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal()
    def __init__(self, parent: PySide6.QtWidgets.QWidget | None = None) -> None:
        super(MachineLoadSuccessStateView, self).__init__(parent = parent)
        self.__state: MachineLoadSuccessState | None = None
        self.__is_online_panel = PySide6.QtWidgets.QLabel('--') 
        self.__vrde_host_panel = PySide6.QtWidgets.QLabel('--')
        self.__vrde_port_panel = PySide6.QtWidgets.QLabel('--')
        self.__start_button = PySide6.QtWidgets.QPushButton('Start')
        self.__stop_button = PySide6.QtWidgets.QPushButton('Stop')

        self.__is_online_panel.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.__vrde_host_panel.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.__vrde_port_panel.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.__start_button.clicked.connect(self.start_machine_request.emit)
        self.__stop_button.clicked.connect(self.stop_machine_request.emit)

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__elements_layout = PySide6.QtWidgets.QGridLayout()
        self.__elements_layout.addWidget(self.__start_button, 0, 0, 1, 2)
        self.__elements_layout.addWidget(self.__stop_button, 1, 0, 1, 2)
        self.__elements_layout.addWidget(PySide6.QtWidgets.QLabel('Status:'), 2, 0, 1, 1)
        self.__elements_layout.addWidget(self.__is_online_panel, 2, 1, 1, 1)
        self.__elements_layout.addWidget(PySide6.QtWidgets.QLabel('VRDE Host:'), 3, 0, 1, 1)
        self.__elements_layout.addWidget(self.__vrde_host_panel, 3, 1, 1, 1)
        self.__elements_layout.addWidget(PySide6.QtWidgets.QLabel('VRDE Port:'), 4, 0, 1, 1)
        self.__elements_layout.addWidget(self.__vrde_port_panel, 4, 1, 1, 1)
        self.__layout.addLayout(self.__elements_layout)
        self.__layout.addStretch(stretch = 1)
        self.setLayout(self.__layout)
        self.resetState()

    def resetState(self, state: MachineLoadSuccessState | None = None) -> None:
        self.__state = state
        if state is not None:
            self.__is_online_panel.setText('🟩 Running' if self.__state.info.is_online else '🟥 Power off')   
            self.__vrde_host_panel.setText(str(self.__state.info.vrde_connection.host))
            self.__vrde_port_panel.setText(str(self.__state.info.vrde_connection.port))
            self.__start_button.setEnabled(not self.__state.info.is_online)
            self.__stop_button.setEnabled(self.__state.info.is_online)
        else:
            self.__is_online_panel.setText('--')   
            self.__vrde_host_panel.setText('--')
            self.__vrde_port_panel.setText('--')
            self.__start_button.setEnabled(False)
            self.__stop_button.setEnabled(False)
class MachineLoadProcessStateView(PySide6.QtWidgets.QWidget):
    def __init__(self, parent: PySide6.QtWidgets.QWidget | None = None) -> None:
        super(MachineLoadProcessStateView, self).__init__(parent = parent)
        self.__state: MachineLoadProcessState | None = None
        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__layout.addWidget(PySide6.QtWidgets.QLabel('Loading...'))
        self.setLayout(self.__layout)
        self.resetState()

    def resetState(self, state: MachineLoadProcessState | None = None) -> None:
        self.__state = state
class MachineLoadErrorStateView(PySide6.QtWidgets.QWidget):
    def __init__(self, parent: PySide6.QtWidgets.QWidget | None = None) -> None:
        super(MachineLoadErrorStateView, self).__init__(parent = parent)
        self.__state: MachineLoadErrorState | None = None

        self.__load_error_reason_view = PySide6.QtWidgets.QTextEdit()
        self.__load_error_reason_view.setReadOnly(True)
        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__layout.addWidget(PySide6.QtWidgets.QLabel('Load error reason:'))
        self.__layout.addWidget(self.__load_error_reason_view)
        self.setLayout(self.__layout)
        self.resetState()

    def resetState(self, state: MachineLoadErrorState | None = None) -> None:
        self.__state = state
        if self.__state is not None:
            self.__load_error_reason_view.setText(self.__state.reason)
        else:
            self.__load_error_reason_view.setText('--')
class MachineView(PySide6.QtWidgets.QWidget):
    start_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    stop_machine_request: PySide6.QtCore.Signal = PySide6.QtCore.Signal(Connection, Machine)
    def __init__(self, parent: PySide6.QtWidgets.QWidget | None = None) -> None:
        super(MachineView, self).__init__(parent = parent)
        self.__machine: Machine | None = None
        self.__uuid_panel = PySide6.QtWidgets.QLabel('')
        self.__uuid_panel.setTextInteractionFlags(PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse | PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.__load_success_view = MachineLoadSuccessStateView()
        self.__load_process_view = MachineLoadProcessStateView()
        self.__load_error_view = MachineLoadErrorStateView()

        self.__load_success_view.start_machine_request.connect(self.__on_start_machine_clicked)
        self.__load_success_view.stop_machine_request.connect(self.__on_stop_machine_clicked)

        self.__layout = PySide6.QtWidgets.QGridLayout()
        self.__state_layout = PySide6.QtWidgets.QStackedLayout()
        self.__state_layout.addWidget(self.__load_success_view)
        self.__state_layout.addWidget(self.__load_process_view)
        self.__state_layout.addWidget(self.__load_error_view)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel('UUID:'), 0, 0, 1, 1)
        self.__layout.addWidget(self.__uuid_panel, 0, 1, 1, 1)
        self.__layout.addLayout(self.__state_layout, 1, 0, 1, 2)
        self.__layout.setRowStretch(0, 0)
        self.__layout.setRowStretch(1, 1)
        self.setLayout(self.__layout)

        self.resetMachine()

    def resetMachine(self, machine: Machine | None = None) -> None:
        if self.__machine is not None:
            try:
                self.__machine.machine_state_changed.disconnect(self.__update_machine_view)
            except Exception:
                pass
        self.__machine = machine
        if self.__machine is not None:
            self.__machine.machine_state_changed.connect(self.__update_machine_view)
        self.__update_machine_view()
    def __update_machine_view(self) -> None:
        if self.__machine is None:
            self.__uuid_panel.setText(str(uuid.UUID(int = 0)))
            self.__load_error_view.resetState(state = MachineLoadErrorState(reason = 'Has no machine...'))
            self.__state_layout.setCurrentWidget(self.__load_error_view)
        else:
            self.__uuid_panel.setText(str(self.__machine.machine_uuid))
            match type(self.__machine.machine_state):
                case internal.models.machine.MachineLoadSuccessState:
                    self.__load_success_view.resetState(state = self.__machine.machine_state)
                    self.__state_layout.setCurrentWidget(self.__load_success_view)
                case internal.models.machine.MachineLoadProcessState:
                    self.__load_process_view.resetState(state = self.__machine.machine_state)
                    self.__state_layout.setCurrentWidget(self.__load_process_view)
                case internal.models.machine.MachineLoadErrorState:
                    self.__load_error_view.resetState(state = self.__machine.machine_state)
                    self.__state_layout.setCurrentWidget(self.__load_error_view)
                case _:
                    self.__load_error_view.resetState(state = MachineLoadErrorState(reason = 'Has no machine by UUID...'))
                    self.__state_layout.setCurrentWidget(self.__load_error_view)

    def __on_start_machine_clicked(self) -> None:
        self.start_machine_request.emit(self.__machine.parent(), self.__machine)
    def __on_stop_machine_clicked(self) -> None:
        self.stop_machine_request.emit(self.__machine.parent(), self.__machine)
