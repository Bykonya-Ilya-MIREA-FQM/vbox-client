from logging import root
from platform import machine
import PySide6.QtWidgets
from external.vbox_server.src.domain.machines import VrdeConnectionInfo
from external.vbox_server.src.domain.machines.models import CreateMachineInfo, FullMachineInfo
from internal.models.connection import Connection, ConnectionDestination
from internal.models.machine import Machine, MachineLoadProcessState, MachineLoadSuccessState, MachineLoadErrorState
from internal.models.root import Root
from internal.controllers.create_machine import CreateMachineController
from internal.controllers.get_connection_status import GetConnectionStatusController
from internal.controllers.get_machine_list import GetMachineListController
from internal.controllers.get_machine_info import GetMachineInfoController
from internal.controllers.delete_machine import DeleteMachineController
from internal.controllers.start_machine import StartMachineController
from internal.controllers.stop_machine import StopMachineController
from internal.views.connection import ConnectionView
from internal.views.machine import MachineView
from internal.views.root import RootView
import PySide6.QtConcurrent
import PySide6.QtAsyncio
import PySide6.QtQuick
import PySide6.QtCore
import PySide6.QtQml
import PySide6.QtGui
import qt_material
import asyncio
import uuid
import sys

# async def test():
#     await GetConnectionStatusController().exec(connection = ConnectionInfo(host = '127.0.0.1', port = 44444))
#     await GetMachineListController().exec(connection = ConnectionInfo(host = '127.0.0.1', port = 44444))
#     await GetMachineInfoController().exec(connection = ConnectionInfo(host = '127.0.0.1', port = 44444), machine_uuid = '2a3aa679-a05e-4872-8086-2cc0e5e5a280')

if __name__ == "__main__":
    application = PySide6.QtWidgets.QApplication(sys.argv)
    
    application.setFont(PySide6.QtGui.QFontDatabase.systemFont(PySide6.QtGui.QFontDatabase.SystemFont.FixedFont))
    qt_material.apply_stylesheet(app = application, theme = 'dark_lightgreen.xml', invert_secondary = True, extra = {
        # Font
        'font_family': 'monospace',
        'line_height': '14px',
        'font_size': '14px',
        # Density Scale
        'density_scale': '0',
        # environ
        'PySide6': True,
        'windows': True,
    })

    connections = Root()
    root_view = RootView(model = connections)
    connection_view = ConnectionView()
    machine_view = MachineView()

    root_view.current_connection_changed.connect(connection_view.resetConnection)
    connection_view.current_machine_changed.connect(machine_view.resetMachine)

    root_view.create_connection_request.connect(lambda connection_destination: GetConnectionStatusController().exec(connection = connections.create_connection(connection_destination = connection_destination)))
    root_view.update_connection_request.connect(lambda connection: GetConnectionStatusController().exec(connection = connection))
    root_view.delete_connection_request.connect(lambda connection: connections.delete_connection(connection_destination = connection.connection_destination))

    connection_view.create_machine_request.connect(lambda connection, create_machine_info: CreateMachineController().exec(connection = connection, machine_info = create_machine_info))
    connection_view.update_all_machine_request.connect(lambda connection: GetMachineListController().exec(connection = connection))
    connection_view.update_one_machine_request.connect(lambda connection, machine: GetMachineInfoController().exec(connection = connection, machine = machine))
    connection_view.delete_machine_request.connect(lambda connection, machine: DeleteMachineController().exec(connection, machine = machine))
    connection_view.start_machine_request.connect(lambda connection, machine: StartMachineController().exec(connection, machine = machine))
    connection_view.stop_machine_request.connect(lambda connection, machine: StopMachineController().exec(connection, machine = machine))
    machine_view.start_machine_request.connect(lambda connection, machine: StartMachineController().exec(connection, machine = machine))
    machine_view.stop_machine_request.connect(lambda connection, machine: StopMachineController().exec(connection, machine = machine))

    window = PySide6.QtWidgets.QWidget()
    layout = PySide6.QtWidgets.QHBoxLayout()
    layout.addWidget(root_view, 1)
    layout.addWidget(connection_view, 1)
    layout.addWidget(machine_view, 1)
    window.setLayout(layout)
    window.show()
    sys.exit(PySide6.QtAsyncio.run())
