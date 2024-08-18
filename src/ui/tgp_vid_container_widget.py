from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSlider,
                             QVBoxLayout, QWidget)


class TgpVidContainerWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.is_tgp_shown = True

        self.tgp_label = QLabel(self)
        self.tgp_label.setAlignment(Qt.AlignCenter)

        tgp_container_layout = QVBoxLayout(self)
        tgp_container_layout.addWidget(self.tgp_label)
        self.tgp_container_widget = QWidget(self)
        self.tgp_container_widget.setLayout(tgp_container_layout)

        video_widget = QVideoWidget(self)
        self.video_player = QMediaPlayer(self)
        self.video_player.setVideoOutput(video_widget)
        self.play_button = QPushButton("Play", self)
        self.mute_button = QPushButton("Mute", self)
        self.slider = QSlider(Qt.Horizontal, self)

        video_control_layout = QHBoxLayout()
        video_control_layout.addWidget(self.play_button)
        video_control_layout.addWidget(self.mute_button)
        video_control_layout.addWidget(self.slider)

        video_player_layout = QVBoxLayout()
        video_player_layout.addWidget(video_widget)
        video_player_layout.addLayout(video_control_layout)

        self.video_container_widget = QWidget(self)
        self.video_container_widget.setLayout(video_player_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_container_widget)
        layout.addWidget(self.tgp_container_widget)

        layout.setContentsMargins(0, 0, 0, 0)

        self.play_button.clicked.connect(self.toggle_play_pause)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)
        self.video_player.positionChanged.connect(self.update_position)

        self.video_container_widget.hide()

    def set_video(self, video_path: str) -> None:
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

    def set_tgp(self, tgp_path: str) -> None:
        pixmap = QPixmap(tgp_path)
        self.tgp_label.setPixmap(pixmap)
        self.tgp_label.setPixmap(pixmap.scaled(self.tgp_label.size(), Qt.KeepAspectRatio))

    def is_playing(self) -> bool:
        return self.video_player.state() == QMediaPlayer.PlayingState

    def toggle_play_pause(self) -> None:
        if self.is_tgp_shown:
            return

        if self.is_playing():
            self.video_player.pause()
            self.play_button.setText("Play")
        else:
            self.video_player.play()
            self.play_button.setText("Pause")

    def toggle_mute(self) -> None:
        if self.is_tgp_shown:
            return

        if self.video_player.isMuted():
            self.video_player.setMuted(False)
            self.mute_button.setText("Mute")
        else:
            self.video_player.setMuted(True)
            self.mute_button.setText("Unmute")

    def set_position(self, position: int) -> None:
        if self.video_player.duration() > 0:
            self.video_player.setPosition(position * self.video_player.duration() // 100)

    def update_position(self, position: int) -> None:
        if self.video_player.duration() > 0:
            self.slider.setValue(int(position * 100 // self.video_player.duration()))

    def seek_to_percentage(self, percentage: int) -> None:
        if self.is_tgp_shown:
            return

        if self.video_player.duration() > 0:
            self.video_player.setPosition(
                int(self.video_player.duration() * percentage // 100))

    def toggle_tgp_vid(self) -> None:
        if self.is_tgp_shown:
            self.is_tgp_shown = False
            self.tgp_container_widget.hide()
            self.video_container_widget.show()
        else:
            self.is_tgp_shown = True
            if self.is_playing():
                self.video_player.pause()
            self.video_container_widget.hide()
            self.tgp_container_widget.show()
