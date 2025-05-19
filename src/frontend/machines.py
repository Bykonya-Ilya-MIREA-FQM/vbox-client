from frontend.utils.current_watching_list_view import CurrentWatchingListView
import backend.model.machines
import PySide6.QtWidgets
import PySide6.QtCore


class MachinesView(PySide6.QtWidgets.QWidget):
    current_machine_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(PySide6.QtCore.QModelIndex)
    def __init__(self, parent: PySide6.QtCore.QObject | None = None) -> None:
        super(MachinesView, self).__init__(parent = parent)
        self.__list_view = CurrentWatchingListView()
        self.__list_view.setSelectionBehavior(PySide6.QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)
        self.__list_view.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.__list_view.current_item_changed.connect(self.current_machine_changed.emit)

        self.__layout = PySide6.QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.__list_view)
        self.setLayout(self.__layout)
        
        self.resetMachineModel()

    def resetMachineModel(self, model: backend.model.machines.MachinesModel | None = None) -> None:
        self.__list_view.setModel(model)
