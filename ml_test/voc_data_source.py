"""For working with data from http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#data
"""

from pathlib import Path


class VOCDataSource:
    def __init__(self, voc_path):
        self._voc_path = Path(voc_path)
        self._image_dir = self._voc_path / 'JPEGImages'
        self._mask_dir = self._voc_path / 'SegmentationClass'

    def __iter__(self):
        for mask in self._mask_dir.iterdir():
            yield (self._image_dir / f'{mask.stem}.jpg', mask)
