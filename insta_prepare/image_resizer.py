from typing import Tuple, TYPE_CHECKING, Optional

from PIL import Image, ImageColor

if TYPE_CHECKING:
    from PIL.JpegImagePlugin import JpegImageFile


class ImageResizer:
    suffix = "_prepared"

    MAX_SIDE_SIZE = 1080

    def __init__(
        self, photo: "JpegImageFile", square_color: Optional[str] = None
    ) -> None:
        self._photo = photo
        self.max_side_size: int = max([self._photo.height, self._photo.width])
        self.min_side_size: int = min([self._photo.height, self._photo.width])
        self.photo_sizes_ratio: float = self.max_side_size / self.min_side_size
        self.square_color = square_color

    def __calc_new_size(self) -> Tuple[int, int]:
        if self.__width_is_bigger():
            return self.MAX_SIDE_SIZE, int(self.MAX_SIDE_SIZE / self.photo_sizes_ratio)
        if self._photo.height > self._photo.width:
            return int(self.MAX_SIDE_SIZE / self.photo_sizes_ratio), self.MAX_SIDE_SIZE
        else:
            return self.MAX_SIDE_SIZE, self.MAX_SIDE_SIZE

    def get_processed_image(self) -> "JpegImageFile":
        new_width, new_height = self.__calc_new_size()
        image = self._photo.resize((new_width, new_height), Image.ANTIALIAS)
        if self.square_color and not (self._photo.height == self._photo.width):
            bkg_color = ImageColor.getrgb(self.square_color)
            new_image = Image.new(
                image.mode, (self.MAX_SIDE_SIZE, self.MAX_SIDE_SIZE), bkg_color
            )
            if self.__width_is_bigger():
                position_to_paste = (0, (self.MAX_SIDE_SIZE // 2 - new_height // 2))
            else:
                position_to_paste = ((self.MAX_SIDE_SIZE // 2 - new_width // 2), 0)
            new_image.paste(image, position_to_paste)
            return new_image
        return image

    def __width_is_bigger(self) -> bool:
        return self._photo.width > self._photo.height

    def __height_is_bigger(self) -> bool:
        return self._photo.height > self._photo.width
