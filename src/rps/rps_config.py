"""
RPS config related functionality
"""

import json
from pathlib import Path
from typing import Any, Dict, List


class RpsConfig:
    """RPS config class"""

    def __init__(self) -> None:
        """Initialize RpsConfig class"""

        config_data = self._get_config_data()

        self.static_path = config_data["static_path"]

        self.video_names = self._get_video_names()
        self.gallery_names = self._get_gallery_names()
        self.tag_names = config_data["tags"]

        self.video_galleries = self._get_video_galleries(config_data["video_relations"])
        self.video_tags = self._get_video_tags(config_data["video_relations"])

        self.gallery_images = {}
        for gallery_name in self.gallery_names:
            self.gallery_images[gallery_name] = self._get_gallery_images(gallery_name)

    def _get_video_names(self) -> List[str]:
        """Get video filenames from static path

        Returns:
            List[str]: Video filenames
        """
        videos_path = Path(self.static_path) / 'VID'
        video_names = []
        for video_path in videos_path.iterdir():
            if video_path.is_file() and video_path.name[0] != '.':
                video_names.append(video_path.name)
        return video_names

    def _get_gallery_names(self) -> List[str]:
        """Get gallery directory names from static path

        Returns:
            List[str]: Gallery directory names
        """
        galleries_path = Path(self.static_path) / 'NAM'
        gallery_names = []
        for gallery_path in galleries_path.iterdir():
            if gallery_path.is_dir() and gallery_path.name[0] != '.':
                gallery_names.append(gallery_path.name)
        return gallery_names

    def _get_video_galleries(self, video_relations: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
        """Get galleries for a video

        Args:
            video_name (str): Video filename

        Returns:
            Dict[str, List[str]]: Galleries attached to each video
        """
        video_galleries = {}
        for video_name in self.video_names:
            if video_name not in video_relations:
                video_galleries[video_name] = self.gallery_names[:]
            else:
                video_galleries[video_name] = []
                for gallery_name in video_relations[video_name]["galleries"]:
                    if gallery_name in self.gallery_names:
                        video_galleries[video_name].append(gallery_name)

        return video_galleries

    def _get_video_tags(self, video_relations: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
        """Get tags for a video

        Returns:
            Dict[str, List[str]]: Tags attached to each video
        """
        video_tags = {}
        for video_name in self.video_names:
            if video_name not in video_relations:
                video_tags[video_name] = self.tag_names[:]
            else:
                video_tags[video_name] = []
                for tag_name in video_relations[video_name]["tags"]:
                    if tag_name in self.tag_names:
                        video_tags[video_name].append(tag_name)

        return video_tags

    def _get_config_data(self) -> Dict[str, Any]:
        """Returns data from config file

        Raises:
            FileNotFoundError: if config file not found
            KeyError: if required keys not found in config

        Returns:
            dict[str, Any]: static path where the media files are located
        """
        config_file = Path.home() / 'pvorg-qt.json'
        if not config_file.exists():
            raise FileNotFoundError(f'Config file not found: {config_file}')

        config_data = {}
        with config_file.open() as file:
            data = json.loads(file.read())
            if "staticPath" in data:
                config_data["static_path"] = data["staticPath"]
            else:
                raise KeyError("'staticPath' not found in config")
            if "videoRelations" in data:
                config_data["video_relations"] = data["videoRelations"]
            else:
                config_data["video_relations"] = {}
            if "tags" in data:
                config_data["tags"] = data["tags"]
            else:
                config_data["tags"] = []

        return config_data

    def _get_gallery_images(self, gallery_name: str) -> List[str]:
        image_list = []
        image_exts = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        gallery_path = Path(self.static_path) / "NAM" / gallery_name
        for filename in gallery_path.iterdir():
            if filename.suffix.lower() in image_exts:
                image_list.append(str(filename))
        return image_list
