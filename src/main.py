from typing import Any, Set
from PyQt5.QtCore import Qt
from pathlib import Path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from rps.combs import get_combinations
from rps.rps_config import RpsConfig

from ui.main_widget import MainWidget


class Main(QMainWindow):
    def __init__(self) -> None:
        self.rps_config = RpsConfig()

        super().__init__()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.main_widget = MainWidget(self.go_prev_combination, self.go_next_combination)
        layout.addWidget(self.main_widget)

        self.setWindowTitle("PVORG")

        self.setup_data()

    def setup_data(self) -> None:
        self.selected_videos = set(self.rps_config.video_names)
        self.selected_galleries = set(self.rps_config.gallery_names)
        self.selected_tags: Set[str] = set()

        self.combinations = get_combinations(
            self.selected_videos, self.selected_galleries, self.selected_tags, self.rps_config)
        self.combination_index = 0
        if len(self.combinations) > 0:
            self.update_combination()

    def go_prev_combination(self) -> None:
        self.navigate_combination(-1)

    def go_next_combination(self) -> None:
        self.navigate_combination(1)

    def navigate_combination(self, diff: int) -> None:
        if len(self.combinations) == 0:
            return
        self.combination_index = (self.combination_index + diff) % len(self.combinations)
        self.update_combination()

    def update_combination(self) -> None:
        if len(self.combinations) == 0:
            return
        video, gallery = self.combinations[self.combination_index]
        self.main_widget.view_tab_widget.control_bar_widget.set_vid_name(video)
        self.main_widget.view_tab_widget.control_bar_widget.set_gal_name(gallery)
        self.main_widget.view_tab_widget.display_media_widget.gallery_container_widget.set_image_list(
            self.rps_config.gallery_images[gallery])

        self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.set_video(
            str(Path(self.rps_config.static_path) / "VID" / video))
        self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.set_tgp(
            str(Path(self.rps_config.static_path) / "VID" / "img" / (video + ".jpg")))

    def keyPressEvent(self, event: Any) -> None:
        if event.key() in range(Qt.Key_0, Qt.Key_9 + 1):  # Keys 1 to 9
            percentage = (event.key() - Qt.Key_0) * 10
            self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.seek_to_percentage(
                percentage)
        elif event.key() == Qt.Key_M:
            self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.toggle_mute()
        elif event.key() == Qt.Key_P:
            if self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.is_playing():
                self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.toggle_play_pause()
                self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.toggle_tgp_vid()
            else:
                self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.toggle_tgp_vid()
                self.main_widget.view_tab_widget.display_media_widget.tgp_vid_container_widget.toggle_play_pause()
        elif event.key() == Qt.Key_N:
            self.go_next_combination()
        elif event.key() == Qt.Key_B:
            self.go_prev_combination()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
