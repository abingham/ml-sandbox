from itertools import islice
from pathlib import Path
import shutil


IMAGE_INPUT_DIR = Path('../data/VOCdevkit/VOC2012') / 'JPEGImages'
MASK_INPUT_DIR = Path('../data/VOCdevkit/VOC2012') / 'SegmentationClass'

DATA_ROOT = Path('data')
TRAINING_IMAGE_DIR = DATA_ROOT / 'training_images'
TRAINING_MASK_DIR = DATA_ROOT / 'training_masks'
VALIDATION_IMAGE_DIR = DATA_ROOT / 'validation_images'
VALIDATION_MASK_DIR = DATA_ROOT / 'validation_masks'
TESTING_IMAGE_DIR = DATA_ROOT / 'test_images'
TESTING_MASK_DIR = DATA_ROOT / 'test_masks'


def num_images():
    return len(tuple(MASK_INPUT_DIR.iterdir()))


def input_data():
    for mask in MASK_INPUT_DIR.iterdir():
        yield (IMAGE_INPUT_DIR / f'{mask.stem}.jpg', mask)


def main():
    training_split = int(0.7 * num_images())
    validation_split = int(0.9 * num_images())

    data_sets = {
        (TRAINING_IMAGE_DIR, TRAINING_MASK_DIR): islice(input_data(), training_split),
        (VALIDATION_IMAGE_DIR, VALIDATION_MASK_DIR): islice(input_data(), training_split, validation_split),
        (TESTING_IMAGE_DIR, TESTING_MASK_DIR): islice(input_data(), validation_split, num_images()),
    }
    for (img_dir, mask_dir), inputs in data_sets.items():
        img_dir.mkdir(parents=True)
        mask_dir.mkdir(parents=True)
        for img, mask in inputs:
            shutil.copy(img, img_dir)
            shutil.copy(mask, mask_dir)


if __name__ == '__main__':
    main()

