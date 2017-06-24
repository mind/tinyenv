from __future__ import absolute_import, division, print_function

import argparse
import json
import os
# from pkg_resources import resource_filename


def flags():
    parser = argparse.ArgumentParser()
    for fd in _load_flags():
        flag_type = _wrap_type(fd.get('type'))
        if not flag_type:
            continue
        parser.add_argument(
            '--' + fd['name'],
            type=flag_type,
            default=fd.get('value'),
            help=fd.get('desc'),
        )
    args = parser.parse_args()
    return args


def _wrap_type(typestr):
    if typestr == 'int':
        return int
    if typestr == 'float':
        return float
    if typestr == 'string':
        return str
    if typestr == 'bool':
        return bool
    return None


def _load_flags():
    """Load flag definitions.

    It will first attempt to load the file at TINYFLAGS environment variable.
    If that does not exist, it will then load the default flags file bundled
    with this library.

    :returns list: Flag definitions to use.
    """
    path = os.getenv('TINYFLAGS')
    if path and os.path.exists(path) and not os.path.isdir(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return []
    # with open(resource_filename('tinyenv', 'config/flags.json'), 'r') as f:
    #     return json.load(f)
