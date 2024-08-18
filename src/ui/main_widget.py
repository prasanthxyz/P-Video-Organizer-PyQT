from typing import Callable
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.config_tab_widget import ConfigTabWidget
from ui.view_tab_widget import ViewTabWidget


class MainWidget(QWidget):
    def __init__(self, go_prev_combination: Callable[..., None], go_next_combination: Callable[..., None]) -> None:
        super().__init__()

        self.view_tab_widget = ViewTabWidget(go_prev_combination, go_next_combination)
        self.config_tab_widget = ConfigTabWidget()

        main_tab_widget = QTabWidget(self)
        main_tab_widget.addTab(self.view_tab_widget, "View")
        main_tab_widget.addTab(self.config_tab_widget, "Config")

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(main_tab_widget)

        layout.setContentsMargins(0, 0, 0, 0)
