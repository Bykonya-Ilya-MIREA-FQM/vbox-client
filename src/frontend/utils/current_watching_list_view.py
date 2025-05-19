import PySide6.QtWidgets
import PySide6.QtCore

class CurrentWatchingListView(PySide6.QtWidgets.QListView):
    current_item_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(PySide6.QtCore.QModelIndex)
    def currentChanged(self, current: PySide6.QtCore.QModelIndex, previous: PySide6.QtCore.QModelIndex) -> None:
        super(CurrentWatchingListView, self).currentChanged(current, previous)
        self.current_item_changed.emit(current)
