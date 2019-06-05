"""Copy the VOC2012 images into the right place.
"""

import sys

from ml_test.data_set import DataSet, copy_in
from ml_test.voc_data_source import VOCDataSource


def main(args):
    source = VOCDataSource(args[1])
    data_set = DataSet('data')
    copy_in(source, data_set)


if __name__ == '__main__':
    main(sys.argv)
