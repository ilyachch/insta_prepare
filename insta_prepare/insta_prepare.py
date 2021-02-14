import argparse
from pathlib import Path
from typing import Tuple, List, TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from PIL.JpegImagePlugin import JpegImageFile


class ImageResizer:
    suffix = '_prepared'

    MAX_SIDE_SIZE = 1080

    def __init__(self, photo: 'JpegImageFile', make_square: bool)-> None:
        self._photo = photo
        self._max_side_size: int = max([self._photo.height, self._photo.width])
        self._min_side_size: int = min([self._photo.height, self._photo.width])
        self._photo_sizes_ratio: float = self._max_side_size / self._min_side_size
        self._make_square = make_square

    def __calc_new_size(self) -> Tuple[int, int]:
        if self.__width_is_bigger():
            return self.MAX_SIDE_SIZE, int(self.MAX_SIDE_SIZE / self._photo_sizes_ratio)
        if self._photo.height > self._photo.width:
            return int(self.MAX_SIDE_SIZE / self._photo_sizes_ratio), self.MAX_SIDE_SIZE
        else:
            return self.MAX_SIDE_SIZE, self.MAX_SIDE_SIZE

    def get_processed_image(self) -> 'JpegImageFile':
        new_width, new_height = self.__calc_new_size()
        image = self._photo.resize((new_width, new_height), Image.ANTIALIAS)
        if self._make_square and not (self._photo.height == self._photo.width):
            new_image = Image.new(image.mode, (self.MAX_SIDE_SIZE, self.MAX_SIDE_SIZE), (0, 0, 0))
            if self.__width_is_bigger():
                position_to_paste = (0, (self.MAX_SIDE_SIZE // 2 - new_height // 2))
            else:
                position_to_paste = ((self.MAX_SIDE_SIZE // 2 - new_width) // 2, 0)
            new_image.paste(image, position_to_paste)
            return new_image
        return image

    def __width_is_bigger(self) -> bool:
        return self._photo.width > self._photo.height

    def __height_is_bigger(self) -> bool:
        return self._photo.height > self._photo.width


def make_args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_process', action='store', default=Path.cwd(), type=Path)
    parser.add_argument('--make-square', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args_parser = make_args_parser()
    folder_to_process: Path = args_parser.path_to_process
    make_images_square: bool = args_parser.make_square
    files_to_process: List[Path] = [f for f in folder_to_process.iterdir() if
                                    (not f.is_dir() and f.suffix in ['.jpg', '.jpeg', '.JPG', '.JPEG'])]
    for image_file in files_to_process:
        file_data = Image.open(image_file)
        new_file_name = f'{image_file.stem}_resized{image_file.suffix}'
        new_image = ImageResizer(file_data, make_images_square).get_processed_image()
        new_image.save(folder_to_process / new_file_name, new_image.format, quality=100)

