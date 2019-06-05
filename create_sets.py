"""Copy the VOC2012 images into the right place.
"""

from itertools import islice
from pathlib import Path
import shutil
import sys


class Copier:
    def __init__(self, voc_path, data_root='data'):
        self._voc_path = Path(voc_path)
        self._data_root = Path(data_root)

        self.IMAGE_INPUT_DIR = self._voc_path / 'JPEGImages'
        self.MASK_INPUT_DIR = self._voc_path / 'SegmentationClass'

        self.TRAINING_IMAGE_DIR = self._data_root / 'training_images'
        self.TRAINING_MASK_DIR = self._data_root / 'training_masks'
        self.VALIDATION_IMAGE_DIR = self._data_root / 'validation_images'
        self.VALIDATION_MASK_DIR = self._data_root / 'validation_masks'
        self.TESTING_IMAGE_DIR = self._data_root / 'test_images'
        self.TESTING_MASK_DIR = self._data_root / 'test_masks'

    def num_images(self):
        return len(tuple(self.MASK_INPUT_DIR.iterdir()))

    def input_data(self):
        for mask in self.MASK_INPUT_DIR.iterdir():
            yield (self.IMAGE_INPUT_DIR / f'{mask.stem}.jpg', mask)

    def copy(self):
        training_split = int(0.7 * self.num_images())
        validation_split = int(0.9 * self.num_images())

        data_sets = {
            (self.TRAINING_IMAGE_DIR, self.TRAINING_MASK_DIR): islice(self.input_data(), training_split),
            (self.VALIDATION_IMAGE_DIR, self.VALIDATION_MASK_DIR): islice(self.input_data(), training_split, validation_split),
            (self.TESTING_IMAGE_DIR, self.TESTING_MASK_DIR): islice(self.input_data(), validation_split, self.num_images()),
        }
        for (img_dir, mask_dir), inputs in data_sets.items():
            img_dir.mkdir(parents=True)
            mask_dir.mkdir(parents=True)
            for img, mask in inputs:
                shutil.copy(img, img_dir)
                shutil.copy(mask, mask_dir)


def main(args):
    c = Copier(args[1])
    c.copy()


if __name__ == '__main__':
    main(sys.argv)
