# Copyright 2019, Cray Inc. All rights reserved.
""" Util functions """
# pylint: disable=invalid-name

import os
import errno

from yaml import safe_load


def get_yaml_file(file):
    """ Make sure the yaml file exists then open it and return it as a dict """
    if not os.path.exists(file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    with open(file) as fp:
        return safe_load(fp)
