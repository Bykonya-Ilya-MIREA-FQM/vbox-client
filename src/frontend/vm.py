import uuid
import backend.model.machines
import PySide6.QtWidgets
import PySide6.QtCore

class VmView(PySide6.QtWidgets.QWidget):
    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(VmView, self).__init__(parent = parent)
        self.__uuid_panel = PySide6.QtWidgets.QLabel('--')
        self.__is_online_panel = PySide6.QtWidgets.QLabel('--') 
        self.__vrde_host_panel = PySide6.QtWidgets.QLabel('--')
        self.__vrde_port_panel = PySide6.QtWidgets.QLabel('--')
        self.__start_button = PySide6.QtWidgets.QPushButton('Start')
        self.__stop_button = PySide6.QtWidgets.QPushButton('Stop')   
        self.__index: PySide6.QtCore.QModelIndex | None = None

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.__uuid_panel)
        self.__layout.addWidget(self.__is_online_panel)
        self.__layout.addWidget(self.__vrde_host_panel)
        self.__layout.addWidget(self.__vrde_port_panel)
        self.__layout.addWidget(self.__start_button)
        self.__layout.addWidget(self.__stop_button)
        self.setLayout(self.__layout)
        self.resetMachinesModelIndex()

    def resetMachinesModelIndex(self, index: PySide6.QtCore.QModelIndex | None = None) -> None:
        self.__index = index
        if self.__index is None or not self.__index.isValid():
            print('c1')
            self.__uuid_panel.setText('--')
            self.__is_online_panel.setText('--')   
            self.__vrde_host_panel.setText('--')
            self.__vrde_port_panel.setText('--')
            self.__start_button.setEnabled(False)
            self.__stop_button.setEnabled(False)
        else:
            machine_uuid: uuid.UUID = self.__index.data(role = backend.model.machines.MachinesModel.MachinesModelRoles.UUID)
            machine_state: backend.model.machines.MachineLoadProcessState | backend.model.machines.MachineLoadSuccessState | backend.model.machines.MachineLoadErrorState = self.__index.data(role = backend.model.machines.MachinesModel.MachinesModelRoles.STATE)
            print(machine_uuid)
            print(machine_state)
            print(type(machine_state))
            print(isinstance(machine_state, backend.model.machines.MachineLoadProcessState))
            print(isinstance(machine_state, backend.model.machines.MachineLoadSuccessState))
            print(isinstance(machine_state, backend.model.machines.MachineLoadErrorState))
            match type(machine_state):
                case backend.model.machines.MachineLoadProcessState:
                    print('c2')
                    self.__uuid_panel.setText('--')
                    self.__is_online_panel.setText('--')   
                    self.__vrde_host_panel.setText('--')
                    self.__vrde_port_panel.setText('--')
                    self.__start_button.setEnabled(False)
                    self.__stop_button.setEnabled(False)
                case backend.model.machines.MachineLoadSuccessState:
                    print('c3')
                    self.__uuid_panel.setText(str(machine_uuid))
                    self.__is_online_panel.setText(str(machine_state.info.is_online))   
                    self.__vrde_host_panel.setText(str(machine_state.info.vrde_connection.host))
                    self.__vrde_port_panel.setText(str(machine_state.info.vrde_connection.port))
                    self.__start_button.setEnabled(not machine_state.info.is_online)
                    self.__stop_button.setEnabled(machine_state.info.is_online)
                case backend.model.machines.MachineLoadErrorState:
                    print('c4')
                    self.__uuid_panel.setText('--')
                    self.__is_online_panel.setText('--')
                    self.__vrde_host_panel.setText('--')
                    self.__vrde_port_panel.setText('--')
                    self.__start_button.setEnabled(False)
                    self.__stop_button.setEnabled(False)
                case _:
                    print('c5')
                    self.__uuid_panel.setText('--')
                    self.__is_online_panel.setText('--')
                    self.__vrde_host_panel.setText('--')
                    self.__vrde_port_panel.setText('--')
                    self.__start_button.setEnabled(False)
                    self.__stop_button.setEnabled(False)
