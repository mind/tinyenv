"""File handling utilities.

This file contains functions that download and process data files. It is
adopted from the data utility file from Keras library.
"""
from __future__ import absolute_import, division, print_function

import hashlib
import os
import shutil
import tarfile
import zipfile

import requests
from clint.textui.progress import bar


def extract_archive(src_path, dst_path='.', archive_format='auto'):
    """Extract an archive if it matches tar, tar.gz, tar.bz, or zip formats.

    :param string src_path: The source path (where the file is at).
    :param string dst_path: The destination path (where to extract to).
    :param string archive_format: The archive format. Options are auto, tar,
        and zip. If auto, both tar and zip will be tried.
    :returns bool: True if the archive is extracted, False otherwise.
    """
    formats = ['tar', 'zip'] if archive_format is 'auto' else [archive_format]
    for fmt in formats:
        if fmt is 'tar':
            open_fn = tarfile.open
            is_match_fn = tarfile.is_tarfile
        if fmt is 'zip':
            open_fn = zipfile.ZipFile
            is_match_fn = zipfile.is_zipfile

        if not is_match_fn(src_path):
            continue

        with open_fn(src_path) as archive:
            try:
                archive.extractall(dst_path)
            except (tarfile.TarError, RuntimeError, KeyboardInterrupt):
                if os.path.exists(dst_path):
                    if os.path.isfile(dst_path):
                        os.remove(dst_path)
                    else:
                        shutil.rmtree(dst_path)
                raise
        return True
    return False


def get_file(fname, url, fhash=None, basedir=None, cachedir='datasets',
             hash_algo='auto', extract=False, archive_format='auto'):
    """Downloads a file from a URL if it not already in the cache.

    :param string fname: The name of the file. If an absolute path is provided,
        the file will be stored at that location.
    :param string url: The URL to download the file from.
    :param string fhash: The expected hash string of the file.
    :param string cachedir: The subfolder of basedir to store caches.
    :param string hash_algo: The hash algorithm to use. sha256, md5 or auto.
    :param bool extract: If True, attempts to extract the file.
    :param string archive_format: If extract is True, specifies the format of
        the archive. tar, zip or auto.
    :returns string: The path to the desired file.
    """
    # Prepare the directory that will contain the data file.
    if basedir is None:
        basedir = os.path.expanduser(os.path.join('~', '.tinymind'))
    basedir = os.path.expanduser(basedir)
    if not os.access(basedir, os.W_OK):
        basedir = os.path.join('/tmp', '.tinymind')
    datadir = os.path.join(basedir, cachedir)
    if not os.path.exists(datadir):
        os.makedirs(datadir)
    path = os.path.join(datadir, fname)

    # Check whether a cache exists.
    download = False
    if os.path.exists(path):
        download = fhash and not validate_file(path, fhash, algo=hash_algo)
    else:
        download = True

    if download:
        download_file(url, path)
    if extract:
        extract_archive(path, datadir, archive_format)

    return path


def download_file(url, path):
    """Download a file.

    :param string url: The URL of the remote file.
    :param string path: The path to save the file to.
    """
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        size = int(r.headers.get('content-length')) / 1024 + 1
        for chunk in bar(r.iter_content(chunk_size=8192), expected_size=size):
            if chunk:
                f.write(chunk)
                f.flush()


def hash_file(path, algo='sha256', chunk_size=65535):
    """Calculate a file sha256 or md5 hash.

    :param string path: The path to the file.
    :param string algo: The hashing algorithm to use. Either sha256 or md5.
    :param int chunk_size: The number of bytes to read at a time.
    :returns string: The file hash.
    """
    hasher = hashlib.sha256() if algo is 'sha256' else hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_file(path, file_hash, algo='auto', chunk_size=65535):
    """Validate a file against a sha256 or md5 hash.

    :param string path: The path to the file.
    :param string file_hash: The expected hash value.
    :param string algo: The hashing algorithm to use. sha256, md5, or auto.
    :param int chunk_size: The number of bytes to read at a time.
    :returns bool: Whether the hash is valid.
    """
    hasher = 'sha256' if algo is 'auto' and len(file_hash) is 64 else algo
    return str(hash_file(path, hasher, chunk_size)) == str(file_hash)
