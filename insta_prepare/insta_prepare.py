import argparse
from pathlib import Path
from typing import Tuple, List

from PIL import Image


class ImageResizer:
    WIDTH = 'width'
    HEIGHT = 'height'

    suffix = '_prepared'

    MAX_SIDE_SIZE = 1080

    def __init__(self, photo: Image, new_file_name: str) -> None:
        self.__photo = photo
        self.__max_side_size: int = max([self.__photo.height, self.__photo.width])
        self.__min_size_size: int = min([self.__photo.height, self.__photo.width])
        self.__max_side_name: str = self.WIDTH if self.__max_side_size == self.__photo.width else self.HEIGHT
        self.__min_side_name: str = self.WIDTH if self.__min_side_name == self.__photo.width else self.HEIGHT
        self.__photo_sizes_ratio = self.__max_side_size / self.__min_size_size
        self.new_file = new_file_name

    def __calc_new_size(self) -> Tuple[int, int]:
        if self.__max_side_name == self.WIDTH:
            return self.MAX_SIDE_SIZE, int(self.MAX_SIDE_SIZE / self.__photo_sizes_ratio)
        elif self.__max_side_name == self.HEIGHT:
            return int(self.MAX_SIDE_SIZE / self.__photo_sizes_ratio), self.MAX_SIDE_SIZE
        else:
            return self.MAX_SIDE_SIZE, self.MAX_SIDE_SIZE

    def process_image(self) -> None:
        image = self.__photo.resize(self.__calc_new_size(), Image.ANTIALIAS)
        image.save(self.new_file, 'JPEG', quality=100)


def make_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_process', action='store', default=Path.cwd(), type=Path)
    return parser.parse_args()


if __name__ == '__main__':
    folder_to_process: Path = make_args_parser().path_to_process
    files_to_process: List[Path] = [f for f in folder_to_process.iterdir() if
                                    (not f.is_dir() and f.suffix in ['.jpg', '.jpeg', '.JPG', '.JPEG'])]
    for image_file in files_to_process:
        file_data = Image.open(image_file)
        new_file_name = f'{image_file.stem}_resized{image_file.suffix}'
        ImageResizer(file_data, new_file_name).process_image()
