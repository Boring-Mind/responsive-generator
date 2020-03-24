from os import path
from wand.image import Image

# ToDo: add python 3.8
# Python 3.8 needed
# from typing import TypedDict


# Holds path to 'images' dir
IMG_DIR = path.join(
    # path to the current module folder
    path.abspath(path.dirname(__file__)),
    'images'
)


SIZES = (
    {'label': 'xs', 'width': 640, 'height': 360},
    {'label': 's', 'width': 960, 'height': 540},
    {'label': 'm', 'width': 1280, 'height': 720},
    {'label': 'l', 'width': 1600, 'height': 900}
)


# class Size(TypedDict):
#     """Defines structure of sizes dictionary."""

#     label: str
#     width: int
#     height: int


class ImageVariants():
    def __init__(self, filepath: str):
        """ImageVariants constructor.
        
        filepath: path to the base image file.
                  Images would be saved to the same path
        """
        self.filepath = filepath

    def resize(self, image: Image, size):
        """Fit image to the according size.
        
        If larger, than (width x height),
        fit within box, preserving aspect ratio
        """
        image.transform(resize=f'{size["width"]}x{size["height"]}>')

    def get_new_filepath(self, size) -> str:
        """Generate filepath for new image variant.
        
        size: element of SIZES array. Needed to get size label.

        example of returned path: /home/user/images/image-xs.jpg
        """
        name, extension = path.splitext(self.filepath)
        return f"{name}-{size['label']}{extension}"

    def make_variant(self, base_img: Image, size):
        """Make image variant to handle responsive images.

        base_img: large reference image, that needs to be
                  adjusted for desired resolution

        Function can return only one variant.
        If you need to form plenty of images, use make_variants instead.
        """
        with base_img.clone() as variant:
            self.resize(variant, size)
            new_path = self.get_new_filepath(size)
            variant.save(filename=new_path)
            return new_path

    def make_variants(self):
        """Make variants of image for different screen sizes.

        ToDo: Add sizes import from json
        """
        paths = []
        with Image(filename=self.filepath) as base_image:
            for size in SIZES:
                paths.append(self.make_variant(base_image, size))
        return paths


def main():
    """Example of workflow."""
    image = '1,6.jpg'
    filepath = path.join(IMG_DIR, image)

    mv = ImageVariants(filepath)
    multiple_paths = mv.make_variants()

    image = '1,5.jpg'
    filepath = path.join(IMG_DIR, image)

    sv = ImageVariants(filepath)
    with Image(filename=filepath) as base_img:
        single_path = sv.make_variant(base_img, SIZES[0])

    print('Multiple variants:')
    for p in multiple_paths:
        print(p)

    print('Single variant:')
    print(single_path)


if __name__ == '__main__':
    main()
