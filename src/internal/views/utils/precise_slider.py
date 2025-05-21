import PySide6.QtWidgets
import PySide6.QtCore

class HorizontalPreciseSlider(PySide6.QtWidgets.QWidget):
    value_changed: PySide6.QtCore.Signal = PySide6.QtCore.Signal(int)
    def __init__(self, minimum: int, maximum: int, tick_size: int, tick_interval: int, units: str, parent: PySide6.QtWidgets.QWidget | None = None) -> None:
        super(HorizontalPreciseSlider, self).__init__(parent)
        self.__step_size: int = tick_size

        self.__slider_edit = PySide6.QtWidgets.QSlider()
        self.__spinbox_edit = PySide6.QtWidgets.QSpinBox()
        self.__slider_edit.valueChanged.connect(self.__on_value_changed)
        self.__spinbox_edit.valueChanged.connect(self.__on_value_changed)

        self.__spinbox_edit.setRange(minimum, maximum)
        self.__slider_edit.setRange(minimum, maximum)
        self.__slider_edit.setOrientation(PySide6.QtCore.Qt.Orientation.Horizontal)
        self.__slider_edit.setTickPosition(PySide6.QtWidgets.QSlider.TickPosition.TicksAbove)
        self.__slider_edit.setTickInterval(tick_interval)
        self.__slider_edit.setPageStep(2 * tick_size)
        self.__slider_edit.setSingleStep(tick_size)

        self.__layout = PySide6.QtWidgets.QHBoxLayout()
        self.__layout.addWidget(self.__slider_edit)
        self.__layout.addWidget(self.__spinbox_edit)
        self.__layout.addWidget(PySide6.QtWidgets.QLabel(units))
        self.setLayout(self.__layout)

    def value(self) -> int:
        return self.__spinbox_edit.value()

    def __on_value_changed(self, new_value: int) -> None:
        new_value = int(self.__step_size * round(new_value / self.__step_size))
        self.__spinbox_edit.setValue(new_value)
        self.__slider_edit.setValue(new_value)
        self.value_changed.emit(new_value)
