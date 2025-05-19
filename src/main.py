import PySide6.QtWidgets
from external.vbox_server.src.domain.machines import VrdeConnectionInfo
from backend.model.connections import ConnectionsModel, ConnectionInfo
from backend.model.machines import MachinesModel, FullMachineInfo, MachineLoadSuccessState, MachineLoadProcessState, MachineLoadErrorState
from frontend.connections import ConnectionsView
from frontend.machines import MachinesView
from frontend.vm import VmView
import PySide6.QtQuick
import PySide6.QtCore
import PySide6.QtQml
import PySide6.QtGui
import qt_material
import uuid
import sys


if __name__ == "__main__":
    application = PySide6.QtWidgets.QApplication(sys.argv)
    qt_material.apply_stylesheet(app = application, theme = 'dark_cyan.xml', invert_secondary = True)
    w = PySide6.QtWidgets.QListWidget()
    for i in range(10):
        item = PySide6.QtWidgets.QListWidgetItem()
        item.setCheckState(PySide6.QtCore.Qt.CheckState.Checked if i % 2 == 0 else PySide6.QtCore.Qt.CheckState.Unchecked)
        item.setText(f'i{i}')
        w.addItem(item)
    w.show()

    # connections = ConnectionsModel(connections = [
    #     [ConnectionInfo(host = '178.208.86.244', port = 44444), MachinesModel(is_online = True, machines = [
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = True, vrde_connection = VrdeConnectionInfo(host = '178.208.86.244', port = 50001)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = False, vrde_connection = VrdeConnectionInfo(host = '178.208.86.244', port = 50002)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = True, vrde_connection = VrdeConnectionInfo(host = '178.208.86.244', port = 50003)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = False, vrde_connection = VrdeConnectionInfo(host = '178.208.86.244', port = 50004)))),
    #     ])],
    #     [ConnectionInfo(host = '127.0.0.1', port = 44444), MachinesModel(is_online = False, machines = [
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = True, vrde_connection = VrdeConnectionInfo(host = '127.0.0.1', port = 40001)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = False, vrde_connection = VrdeConnectionInfo(host = '127.0.0.1', port = 40002)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = True, vrde_connection = VrdeConnectionInfo(host = '127.0.0.1', port = 40003)))),
    #         (uuid.uuid4(), MachineLoadSuccessState(info = FullMachineInfo(is_online = False, vrde_connection = VrdeConnectionInfo(host = '127.0.0.1', port = 40004)))),
    #     ])],
    #     [ConnectionInfo(host = '127.0.0.1', port = 1), MachinesModel(is_online = False, machines = [])],
    #     [ConnectionInfo(host = '127.0.0.1', port = 2), MachinesModel(is_online = False, machines = [])],
    #     [ConnectionInfo(host = '127.0.0.1', port = 3), MachinesModel(is_online = True, machines = [])],
    #     [ConnectionInfo(host = '127.0.0.1', port = 4), MachinesModel(is_online = True, machines = [])],
    # ])


    # connection_view = ConnectionsView(model = connections)
    # machine_view = MachinesView()
    # vm_view = VmView()

    # connection_view.current_connection_changed.connect(lambda index: machine_view.resetMachineModel(model = index.data(role = ConnectionsModel.ConnectionsModelRoles.MACHINE_MODEL)))
    # machine_view.current_machine_changed.connect(lambda index: vm_view.resetMachinesModelIndex(index = index))

    # connection_view.current_connection_changed.connect(print)
    # machine_view.current_machine_changed.connect(print)

    # window = PySide6.QtWidgets.QWidget()
    # layout = PySide6.QtWidgets.QHBoxLayout()
    # layout.addWidget(connection_view, 1)
    # layout.addWidget(machine_view, 1)
    # layout.addWidget(vm_view, 1)
    # window.setLayout(layout)
    # window.show()
    sys.exit(application.exec())
