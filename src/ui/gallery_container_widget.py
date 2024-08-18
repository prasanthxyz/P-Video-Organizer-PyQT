from typing import List
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class GalleryContainerWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.image_list: List[str] = []

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)

        self.current_index = 0

    def set_image_list(self, image_list: List[str]) -> None:
        self.stop_slideshow()
        self.image_list = image_list
        self.start_slideshow()

    def start_slideshow(self) -> None:
        if self.image_list:
            self.current_index = 0
            self.timer.start(2000)
            self.show_next_image()

    def stop_slideshow(self) -> None:
        self.timer.stop()

    def show_next_image(self) -> None:
        if self.image_list:
            pixmap = QPixmap(self.image_list[self.current_index])
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            self.current_index = (self.current_index + 1) % len(self.image_list)
