from __future__ import absolute_import, division, print_function

import argparse
import json
import os

from pkg_resources import resource_filename


def flags():
    parser = argparse.ArgumentParser()
    for fd in _load_flags():
        parser.add_argument(
            fd['name'],
            help=fd.get('desc'),
        )
    args = parser.parse_args()
    return args


def _load_flags():
    """Load flag definitions.

    It will first attempt to load the file at TINYFLAGS environment variable.
    If that does not exist, it will then load the default flags file bundled
    with this library.

    :returns list: Flag definitions to use.
    """
    path = os.getenv('TINYFLAGS')
    if os.path.exists(path) and not os.path.isdir(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass

    with open(resource_filename('tinyenv', 'config/flags.json'), 'r') as f:
        return json.load(f)
