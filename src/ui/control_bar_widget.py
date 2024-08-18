from typing import Callable
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton


class ControlBarWidget(QWidget):
    def __init__(
            self,
            go_prev_combination: Callable[..., None],
            go_next_combination: Callable[..., None],
            toggle_tgp_vid: Callable[..., None]) -> None:
        super().__init__()

        self.vid_name = QLabel(self)
        spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        toggle_button = QPushButton(text="TGP/VID")

        prev_button = QPushButton(text="Prev")
        next_button = QPushButton(text="Next")
        spacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gal_name = QLabel(self)

        horizontal_box_1 = QHBoxLayout()
        horizontal_box_1.addWidget(self.vid_name)
        horizontal_box_1.addItem(spacer)
        horizontal_box_1.addWidget(toggle_button)
        horizontal_box_1.setStretch(1, 1)

        horizontal_box_2 = QHBoxLayout()
        horizontal_box_2.addWidget(prev_button)
        horizontal_box_2.addWidget(next_button)
        horizontal_box_2.addItem(spacer_2)
        horizontal_box_2.addWidget(self.gal_name)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addLayout(horizontal_box_1)
        layout.addLayout(horizontal_box_2)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

        prev_button.clicked.connect(go_prev_combination)
        next_button.clicked.connect(go_next_combination)
        toggle_button.clicked.connect(toggle_tgp_vid)

    def set_vid_name(self, vid_name: str) -> None:
        self.vid_name.setText(vid_name)

    def set_gal_name(self, gal_name: str) -> None:
        self.gal_name.setText(gal_name)
