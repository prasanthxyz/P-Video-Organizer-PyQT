from typing import Callable

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ui.control_bar_widget import ControlBarWidget
from ui.display_media_widget import DisplayMediaWidget


class ViewTabWidget(QWidget):
    def __init__(self, go_prev_combination: Callable[..., None], go_next_combination: Callable[..., None]) -> None:
        super().__init__()

        self.control_bar_widget = ControlBarWidget(go_prev_combination, go_next_combination, self.toggle_tgp_vid)
        self.display_media_widget = DisplayMediaWidget()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.control_bar_widget)
        layout.addWidget(self.display_media_widget)

        layout.setStretch(0, 1)
        layout.setStretch(1, 99)
        layout.setContentsMargins(0, 0, 0, 0)

    def toggle_tgp_vid(self) -> None:
        self.display_media_widget.tgp_vid_container_widget.toggle_tgp_vid()
