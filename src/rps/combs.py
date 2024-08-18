import random
from typing import List, Set, Tuple

from rps.rps_config import RpsConfig


def get_combinations(
        selected_videos: Set[str],
        selected_galleries: Set[str],
        selected_tags: Set[str],
        rps_config: RpsConfig) -> List[Tuple[str, str]]:
    """Get all possible combinations of selected videos and galleries

    Args:
        selected_videos (Set[str]): Selected videos
        selected_galleries (Set[str]): Selected galleries
        selected_tags (Set[str]): Selected tags

    Returns:
        List[Tuple[str, str]]: Shuffled list of video-gallery combinations
    """
    combinations = []
    for video in selected_videos:
        video_galleries = rps_config.video_galleries[video]
        video_tags = rps_config.video_tags[video]
        if len(selected_tags) > 0 and len(selected_tags.intersection(video_tags)) != len(selected_tags):
            continue
        for gallery in video_galleries:
            if gallery in selected_galleries:
                combinations.append((video, gallery))

    random.shuffle(combinations)
    return combinations
