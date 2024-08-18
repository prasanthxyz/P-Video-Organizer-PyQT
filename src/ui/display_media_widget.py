from PyQt5.QtWidgets import QHBoxLayout, QWidget

from ui.gallery_container_widget import GalleryContainerWidget
from ui.tgp_vid_container_widget import TgpVidContainerWidget


class DisplayMediaWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.tgp_vid_container_widget = TgpVidContainerWidget()
        self.gallery_container_widget = GalleryContainerWidget()

        layout = QHBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.tgp_vid_container_widget)
        layout.addWidget(self.gallery_container_widget)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setStretch(0, 3)
        layout.setStretch(1, 1)
