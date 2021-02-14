import argparse
from pathlib import Path
from typing import List, Optional

from PIL import Image

from image_resizer import ImageResizer


def make_args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_to_process", action="store", default=Path.cwd(), type=Path
    )
    parser.add_argument(
        "--square-color", "-S", action="store", required=False, default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    args_parser = make_args_parser()
    folder_to_process: Path = args_parser.path_to_process
    square_color: Optional[str] = args_parser.square_color
    files_to_process: List[Path] = [
        f
        for f in folder_to_process.iterdir()
        if (
            not f.stem.endswith("_resized")
            and not f.is_dir()
            and f.suffix in [".jpg", ".jpeg", ".JPG", ".JPEG"]
        )
    ]
    for image_file in files_to_process:
        file_data = Image.open(image_file)
        new_file_name = f"{image_file.stem}_resized{image_file.suffix}"
        new_image = ImageResizer(file_data, square_color).get_processed_image()
        new_image.save(folder_to_process / new_file_name, new_image.format, quality=100)
