from itertools import islice
from pathlib import Path
import shutil


class DataSet:
    def __init__(self, root):
        self._root = Path(root)
        self.training_image_dir = self._root / 'training_images'
        self.training_mask_dir = self._root / 'training_masks'
        self.validation_image_dir = self._root / 'validation_images'
        self.validation_mask_dir = self._root / 'validation_masks'
        self.testing_image_dir = self._root / 'test_images'
        self.testing_mask_dir = self._root / 'test_masks'


def copy_in(source, data_set, splits=(0.7, 0.9)):
    """Copy a data source into a data set.
    """

    inputs = tuple(source)
    num_inputs = len(inputs)
    training_split = int(splits[0] * num_inputs)
    validation_split = int(splits[1] * num_inputs)

    groups = {
        (data_set.training_image_dir, data_set.training_mask_dir): islice(inputs,
                                                                          training_split),
        (data_set.validation_image_dir, data_set.validation_mask_dir): islice(inputs,
                                                                              training_split,
                                                                              validation_split),
        (data_set.testing_image_dir, data_set.testing_mask_dir): islice(inputs,
                                                                        validation_split,
                                                                        num_inputs),
    }
    for (img_dir, mask_dir), inputs in groups.items():
        img_dir.mkdir(parents=True)
        mask_dir.mkdir(parents=True)
        for img, mask in inputs:
            shutil.copy(img, img_dir)
            shutil.copy(mask, mask_dir)

